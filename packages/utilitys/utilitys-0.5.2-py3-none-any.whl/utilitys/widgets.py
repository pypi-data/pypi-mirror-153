from __future__ import annotations

import html
import logging
import typing as t
import weakref
from textwrap import wrap
from traceback import format_exception
from warnings import warn
import sys

import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph import GraphicsScene
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
from pyqtgraph.graphicsItems.LegendItem import ItemSample
from pyqtgraph.graphicsItems.ScatterPlotItem import drawSymbol
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu
from pyqtgraph.parametertree import Parameter

from utilitys.fns import (
    nameFormatter,
    pascalCaseToTitle,
    paramsFlattened,
    dynamicDocstring,
    getParamChild,
    hookupParamWidget,
    timedExec,
    forceRichText,
    getAnyPgColormap,
    listAllPgColormaps,
)
from utilitys.misc import CompositionMixin
from utilitys.typeoverloads import FilePath
from . import params
from .constants import PrjEnums
from .params.prjparam import PrjParam
from .shims import typing_extensions as t_e

# Taken directly from https://stackoverflow.com/a/20610786/9463643
# Many things can cause this statement to fail
# noinspection PyBroadException
try:
    from pyqtgraph.Qt import QtWidgets
    from qtconsole.rich_jupyter_widget import RichJupyterWidget
    from qtconsole.inprocess import QtInProcessKernelManager
    from IPython.lib import guisupport

except Exception:
    from pyqtgraph.console import ConsoleWidget
else:

    class ConsoleWidget(RichJupyterWidget):
        """Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""

        def __init__(self, text=None, *args, **kwargs):
            if not text is None:
                self.banner = text
            super().__init__(*args, **kwargs)
            self.kernel_manager = kernel_manager = QtInProcessKernelManager()
            kernel_manager.start_kernel()
            # kernel_manager.kernel.gui = 'qt5'
            self.kernel_client = kernel_client = self._kernel_manager.client()
            kernel_client.start_channels()

            def stop():
                kernel_client.stop_channels()
                kernel_manager.shutdown_kernel()

            self.exit_requested.connect(stop)

            namespace = kwargs.get("namespace", {})
            namespace.setdefault("__console__", self)
            self.pushVariables(namespace)
            parent = kwargs.get("parent", None)
            if parent is not None:
                self.setParent(parent)

        def pushVariables(self, variableDict):
            """Given a dictionary containing name / value pairs, push those variables to the IPython console widget"""
            self.kernel_manager.kernel.shell.push(variableDict)

        def clearTerminal(self):
            """Clears the terminal"""
            self._control.clear()

        def printText(self, text):
            """Prints some plain text to the console"""
            self._append_plain_text(text)

        def executeCommand(self, command):
            """Execute a command in the frame of the console widget"""
            self._execute(command, False)


# Sometimes, exceptions in the Ipython stack make it difficult to spawn an ipython console even if it is importable
# Wrap around this issue with a Pyqtgraph console if needed
def safeSpawnDevConsole(win: QtWidgets.QMainWindow = None, **locals):
    """
    Opens a console that allows dynamic interaction with current variables. If IPython
    is on your system, a qt console will be loaded. Otherwise, a (less capable) standard
    pyqtgraph console will be used.
    """
    # "dict" default is to use repr instead of string for internal elements, so expanding
    # into string here ensures repr is not used
    locals.update(win=win)
    nsPrintout = [f"{k}: {v}" for k, v in locals.items()]
    text = f"Starting console with variables:\n" f"{nsPrintout}"
    # Broad exception is fine, fallback is good enough. Too many edge cases to properly diagnose when Pycharm's event
    # loop is sync-able with the Jupyter dev console
    # noinspection PyBroadException
    try:
        console = ConsoleWidget(parent=win, namespace=locals, text=text)
    except Exception:
        # Ipy kernel can have issues for many different reasons. Always be ready to fall back to traditional console
        console = pg.console.ConsoleWidget(parent=win, namespace=locals, text=text)
    console.setWindowFlag(QtCore.Qt.WindowType.Window)
    console.show()


class ScrollableMessageDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        messageType="Information",
        msg="",
        detailedMsg="",
    ):
        super().__init__(parent)
        style = self.style()
        self.setModal(True)

        styleIcon = getattr(style, f"SP_MessageBox{messageType}")
        self.setWindowTitle(messageType)
        self.setWindowIcon(style.standardIcon(styleIcon))

        verticalLayout = QtWidgets.QVBoxLayout(self)

        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtWidgets.QWidget()

        scrollLayout = QtWidgets.QVBoxLayout(scrollAreaWidgetContents)

        # Set to message with trace first so sizing is correct
        msgLbl = QtWidgets.QLabel(detailedMsg, scrollAreaWidgetContents)
        msgLbl.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
            | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        msgLbl.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        scrollLayout.addWidget(
            msgLbl,
            0,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        scrollArea.setWidget(scrollAreaWidgetContents)
        verticalLayout.addWidget(scrollArea)

        btnLayout = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton("Ok", self)
        toggleTrace = QtWidgets.QPushButton("Toggle Details", self)
        btnLayout.addWidget(ok)
        btnLayout.addWidget(toggleTrace)
        spacerItem = QtWidgets.QSpacerItem(
            ok.width(),
            ok.height(),
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        ok.clicked.connect(self.close)

        sh = self.sizeHint()
        newWidth = max(sh.width(), self.width())
        newHeight = max(sh.height(), self.height())
        self.resize(newWidth, newHeight)

        showDetailedMsg = False

        def updateTxt():
            nonlocal showDetailedMsg
            if showDetailedMsg:
                newText = detailedMsg.replace("\n", "<br>")
                msgLbl.setTextFormat(QtCore.Qt.TextFormat.RichText)
            else:
                newLines = msg.splitlines()
                allLines = []
                for line in newLines:
                    if line == "":
                        line = [line]
                    else:
                        line = wrap(line)
                    allLines.extend(line)
                newText = "<br>".join(allLines)
                msgLbl.setTextFormat(QtCore.Qt.TextFormat.RichText)
            showDetailedMsg = not showDetailedMsg
            msgLbl.setText(newText)

        self.msgLbl = msgLbl
        toggleTrace.clicked.connect(lambda: updateTxt())

        btnLayout.addItem(spacerItem)
        verticalLayout.addLayout(btnLayout)
        self.toggleTrace = toggleTrace
        ok.setFocus()
        updateTxt()


class StringListValidator(QtGui.QValidator):
    def __init__(
        self,
        parent=None,
        strList: t.Sequence[str] = None,
        model: QtCore.QStringListModel = None,
        validateCase=False,
    ) -> None:
        super().__init__(parent)
        self.validateCase = validateCase
        self.strList = strList
        self.model = model

    def validate(self, input_: str, pos: int):
        if self.model:
            self.strList = [
                self.model.index(ii, 0).data() for ii in range(self.model.rowCount())
            ]
        strList = cmpStrList = [input_] if self.strList is None else self.strList
        cmpInput = input_
        if not self.validateCase:
            cmpInput = input_.lower()
            cmpStrList = [s.lower() for s in strList]

        try:
            matchIdx = cmpStrList.index(cmpInput)
            input_ = strList[matchIdx]
            state = self.State.Acceptable
        except ValueError:
            if any(cmpInput in str_ for str_ in cmpStrList):
                state = self.State.Intermediate
            else:
                state = self.State.Invalid
        return state, input_, pos


class PopupLineEditor(QtWidgets.QLineEdit):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        model: QtCore.QAbstractItemModel = None,
        placeholderText="Press Tab or type...",
        clearOnComplete=True,
        forceMatch=True,
        validateCase=False,
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholderText)
        self.clearOnComplete = clearOnComplete
        self.forceMatch = forceMatch
        self.validateCase = validateCase
        self.model: QtCore.QAbstractListModel = QtCore.QStringListModel()
        if model is None:
            model = self.model

        self.vdator = StringListValidator(parent=self, validateCase=validateCase)
        self.setValidator(self.vdator)

        self.setModel(model)

    def setModel(self, model: QtCore.QAbstractListModel):
        completer = QtWidgets.QCompleter(model, self)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionRole(QtCore.Qt.ItemDataRole.DisplayRole)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        if self.clearOnComplete:
            completer.activated.connect(lambda: QtCore.QTimer.singleShot(0, self.clear))

        self.textChanged.connect(lambda: self.resetCompleterPrefix())

        self.setCompleter(completer)
        self.model = model
        if self.forceMatch:
            self.vdator.model = model

    # TODO: Get working with next prev focusing for smoother logic
    # def focusNextPrevChild(self, nextChild: bool):
    #   if self.forceMatch and self.text() not in self.completer().model().stringList():
    #     dummyFocusEv = QtGui.QFocusEvent(QtCore.QEvent.FocusOut)
    #     self.focusOutEvent(dummyFocusEv)
    #     return False
    #   return super().focusNextPrevChild(nextChild)

    def _chooseNextCompletion(self, incAmt=1):
        completer = self.completer()
        popup = completer.popup()
        if popup.isVisible() and popup.currentIndex().isValid():
            nextIdx = (completer.currentRow() + incAmt) % completer.completionCount()
            completer.setCurrentRow(nextIdx)
        else:
            completer.complete()
        popup.show()
        popup.setCurrentIndex(completer.currentIndex())
        popup.setFocus()

    def event(self, ev: QtCore.QEvent):
        if ev.type() != ev.KeyPress:
            return super().event(ev)

        ev: QtGui.QKeyEvent
        key = ev.key()
        if key == QtCore.Qt.Key.Key_Tab:
            incAmt = 1
        elif key == QtCore.Qt.Key.Key_Backtab:
            incAmt = -1
        else:
            return super().event(ev)
        self._chooseNextCompletion(incAmt)
        return True

    def focusOutEvent(self, ev: QtGui.QFocusEvent):
        reason = ev.reason()
        if reason in [
            QtCore.Qt.FocusReason.TabFocusReason,
            QtCore.Qt.FocusReason.BacktabFocusReason,
            QtCore.Qt.FocusReason.OtherFocusReason,
        ]:
            # Simulate tabbing through completer options instead of losing focus
            self.setFocus()
            completer = self.completer()
            if completer is None:
                return
            incAmt = 1 if reason == QtCore.Qt.FocusReason.TabFocusReason else -1

            self._chooseNextCompletion(incAmt)
            ev.accept()
            return
        else:
            super().focusOutEvent(ev)

    def clear(self):
        super().clear()

    def resetCompleterPrefix(self):
        if self.text() == "":
            self.completer().setCompletionPrefix("")


class HoverScatter(pg.ScatterPlotItem):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def hoverEvent(self, ev: QtGui.QHoverEvent):
        if not hasattr(ev, "_scenePos"):
            return
        pts = self.pointsAt(ev.position() if hasattr(ev, "position") else ev.localPos())
        if len(pts) > 0:
            pt = pts[-1]
            data = pt.data()
            if isinstance(data, t.Callable):
                # Data hasn't been evaluated yet
                try:
                    data = data()
                    pt.setData(data)
                except Exception as ex:
                    data = None
        else:
            data = None
        self.setToolTip(data)


class _DEFAULT_OWNER:
    pass


"""None is a valid owner, so create a sentinel that's not valid"""
btnCallable = t.Callable[[PrjParam], t.Any]


class ButtonCollection(QtWidgets.QGroupBox):
    def __init__(
        self,
        parent=None,
        title: str = None,
        btnParams: t.Collection[PrjParam] = (),
        btnTriggerFns: t.Union[btnCallable, t.Collection[btnCallable]] = (),
        exclusive=True,
        asToolBtn=True,
        **createOpts,
    ):
        super().__init__(parent)
        self.lastTriggered: t.Optional[PrjParam] = None
        self.uiLayout = QtWidgets.QHBoxLayout(self)
        self.btnGroup = QtWidgets.QButtonGroup(self)
        self.paramToFuncMapping: t.Dict[PrjParam, btnCallable] = dict()
        self.paramToBtnMapping: t.Dict[PrjParam, QtWidgets.QPushButton] = dict()
        self.asToolBtn = asToolBtn
        if title is not None:
            self.setTitle(title)
        self.btnGroup.setExclusive(exclusive)

        if not isinstance(btnTriggerFns, t.Iterable):
            btnTriggerFns = [btnTriggerFns] * len(btnParams)
        for param, fn in zip(btnParams, btnTriggerFns):
            self.createAndAddBtn(param, fn, **createOpts)

    def createAndAddBtn(
        self, btnParam: PrjParam, triggerFn: btnCallable, checkable=False, **createOpts
    ):
        if btnParam in self.paramToBtnMapping:
            # Either already exists or wasn't designed to be a button
            return
        createOpts.setdefault("asToolBtn", self.asToolBtn)
        newBtn = self.createBtn(btnParam, **createOpts)
        if checkable:
            newBtn.setCheckable(True)
            oldTriggerFn = triggerFn
            # If the button is checkable, only call this function when the button is checked
            def newTriggerFn(param: PrjParam):
                if newBtn.isChecked():
                    oldTriggerFn(param)

            triggerFn = newTriggerFn
        newBtn.clicked.connect(lambda: self.callFuncByParam(btnParam))

        self.addBtn(btnParam, newBtn, triggerFn)
        return newBtn

    def clear(self):
        for button in self.paramToBtnMapping.values():
            self.btnGroup.removeButton(button)
            self.uiLayout.removeWidget(button)
            button.deleteLater()

        self.paramToBtnMapping.clear()
        self.paramToFuncMapping.clear()

    def addFromExisting(
        self, other: ButtonCollection, which: t.Collection[PrjParam] = None
    ):
        for (param, btn), func in zip(
            other.paramToBtnMapping.items(), other.paramToFuncMapping.values()
        ):
            if which is None or param in which:
                self.addBtn(param, btn, func)

    def addBtn(self, param: PrjParam, btn: QtWidgets.QPushButton, func: btnCallable):
        self.btnGroup.addButton(btn)
        self.uiLayout.addWidget(btn)
        self.paramToFuncMapping[param] = func
        self.paramToBtnMapping[param] = btn

    @classmethod
    def createBtn(
        cls,
        btnOpts: PrjParam,
        baseBtn: QtWidgets.QAbstractButton = None,
        asToolBtn=False,
        parent=None,
        **kwargs,
    ):
        if asToolBtn:
            btnType = QtWidgets.QToolButton
        else:
            btnType = QtWidgets.QPushButton
        tooltipText = btnOpts.helpText
        if baseBtn is not None:
            newBtn = baseBtn
        else:
            newBtn = btnType(parent)
            newBtn.setText(btnOpts.name)
        if "icon" in btnOpts.opts:
            newBtn.setText("")
            newBtn.setIcon(QtGui.QIcon(str(btnOpts.opts["icon"])))
            tooltipText = btnOpts.addHelpText(btnOpts.name)
        if tooltipText:
            tooltipText = forceRichText(tooltipText)
            newBtn.setToolTip(tooltipText)
        reg = params.pgregistered.ShortcutParameter.REGISTRY
        if reg is not None:
            reg.registerButton(btnOpts, newBtn, **kwargs)
        return newBtn

    def callFuncByParam(self, param: PrjParam):
        if param is None:
            return
        # Ensure function is called in the event it requires a button to be checked
        btn = self.paramToBtnMapping[param]
        if btn.isCheckable():
            btn.setChecked(True)
        self.paramToFuncMapping[param](param)
        self.lastTriggered = param

    def addByParam(self, param: Parameter, copy=True, **registerOpts):
        """
        Adds a button to a group based on the parameter. Also works for group params
        that have an acttion nested.
        """
        for param in paramsFlattened(param):
            curCopy = copy
            if param.type() in ["action", "shortcut"] and param.opts.get(
                "guibtn", True
            ):
                existingBtn = None
                try:
                    existingBtn = next(iter(param.items)).button
                except (StopIteration, AttributeError):
                    curCopy = True
                if curCopy:
                    self.createAndAddBtn(
                        PrjParam(**param.opts),
                        lambda *args: param.activate(),
                        **registerOpts,
                    )
                else:
                    self.addBtn(PrjParam(**param.opts), existingBtn, existingBtn.click)

    @classmethod
    def fromToolsEditors(
        cls,
        editors: t.Sequence[params.ParamEditor],
        title="Tools",
        ownerClctn: ButtonCollection = None,
        **registerOpts,
    ):
        if ownerClctn is None:
            ownerClctn = cls(title=title, exclusive=True)

        for editor in editors:
            ownerClctn.addByParam(editor.params, **registerOpts)

        return ownerClctn

    def toolbarFormat(self):
        """
        Returns a list of buttons + title in a format that's easier to add to a toolbar, e.g.
        doesn't require as much horizontal space
        """
        title = self.title()
        out: t.List[QtWidgets.QWidget] = (
            [] if title is None else [QtWidgets.QLabel(self.title())]
        )
        for btn in self.paramToBtnMapping.values():
            out.append(btn)
        return out


_layoutTypes = t.Union[t_e.Literal["H"], t_e.Literal["V"]]


class EasyWidget:
    def __init__(
        self,
        children: t.MutableSequence,
        layout: str = None,
        useSplitter=False,
        baseWidget: QtWidgets.QWidget = None,
    ):
        if baseWidget is None:
            baseWidget = QtWidgets.QWidget()
        self._built = False
        self.children_ = children
        self.useSplitter = None
        self.widget_ = baseWidget
        self.layout_ = None

        self._resetOpts(useSplitter, layout)

    def _resetOpts(self, useSplitter, layout):
        if layout == "V":
            orient = QtCore.Qt.Orientation.Vertical
            layout = QtWidgets.QVBoxLayout
        elif layout == "H":
            orient = QtCore.Qt.Orientation.Horizontal
            layout = QtWidgets.QHBoxLayout
        else:
            orient = layout = None
        self.orient_ = orient

        if useSplitter == self.useSplitter and self.layout_:
            return
        # Had children in existing widget which will be discarded when changing self widget_ to splitter
        if self.widget_.children() and useSplitter:
            raise ValueError(
                "Cannot change splitter status to *True* when widget already has children"
            )
        self.useSplitter = useSplitter

        if useSplitter:
            self.layout_ = QtWidgets.QSplitter(orient)
            self.widget_ = self.layout_
        else:
            try:
                self.layout_ = layout()
                self.widget_.setLayout(self.layout_)
            except TypeError:
                # When layout is none
                self.layout_ = None

    def build(self):
        if self._built:
            return
        if self.layout_ is None:
            raise ValueError(
                'Top-level orientation must be set to "V" or "H" before adding children'
            )
        if self.orient_ == QtCore.Qt.Orientation.Horizontal:
            chSuggested = "V"
        elif self.orient_ == QtCore.Qt.Orientation.Vertical:
            chSuggested = "H"
        else:
            chSuggested = None

        for ii, child in enumerate(self.children_):
            morphChild = self.addChild(child, chSuggested)
            if morphChild is not child:
                self.children_[ii] = morphChild
        self._built = True

    def addChild(
        self,
        child: t.Union[QtWidgets.QWidget, t.Sequence, EasyWidget],
        suggestedLayout: str = None,
    ):
        if isinstance(child, QtWidgets.QWidget):
            self.layout_.addWidget(child)
        else:
            child = self.listChildrenWrapper(child, suggestedLayout)
            # At this point, child should be an EasyWidget
            child.build()
            self.layout_.addWidget(child.widget_)
        return child

    def insertChild(self, child: EasyWidget, index: int):
        child.build()
        return self.layout_.insertWidget(index, child.widget_)

    def hide(self):
        self.widget_.hide()

    def show(self):
        self.widget_.show()

    def removeInnerMargins(self):
        for ch in self.children_:
            if isinstance(ch, EasyWidget):
                ch.removeInnerMargins()
                lay = ch.widget_.layout()
                # layout_ != widget_.layout() for splitter
                if lay:
                    lay.setContentsMargins(0, 0, 0, 0)
                    lay.setSpacing(0)

    @classmethod
    def listChildrenWrapper(
        cls, children: t.Union[t.Sequence, EasyWidget], maybeNewLayout: str = None
    ):
        if not isinstance(children, EasyWidget):
            children = cls(children)
        if children.layout_ is None and maybeNewLayout is not None:
            children._resetOpts(children.useSplitter, maybeNewLayout)
        return children

    @classmethod
    def buildMainWin(
        cls,
        children: t.Union[t.Sequence, EasyWidget],
        win: QtWidgets.QMainWindow = None,
        layout="V",
        **kwargs,
    ):
        if win is None:
            win = QtWidgets.QMainWindow()
        if isinstance(children, t.Sequence):
            children = cls(children, layout=layout, **kwargs)

        children.build()
        win.easyChild = children
        win: HasEasyChild
        win.setCentralWidget(children.widget_)
        children.removeInnerMargins()
        return win

    @classmethod
    def buildWidget(
        cls, children: t.Union[t.Sequence, EasyWidget], layout="V", **kwargs
    ):
        builder = cls(children, layout=layout, **kwargs)
        builder.build()
        retWidget: HasEasyChild = builder.widget_
        retWidget.easyChild = builder
        builder.removeInnerMargins()
        return retWidget

    @classmethod
    def fromPgParam(cls, param: Parameter = None, layout="H", **opts):
        """
        Creates a form-style EasyWidget (name + edit widget) from pyqtgraph parameter options or a parameter directly.

        :param param: Parameter to use, if it already exists. Otherwise, one is created from `opts` and returned.
        :param layout: EasyWidget layout
        :param opts: If `param` is unspecified, a parameter is created from these opts instead and returned

        :return: Just the EasyWidget if `param` is provided, otherwise (EasyWidget, Parameter) tuple
        """
        returnParam = False
        if param is None:
            param = Parameter.create(**opts)
            returnParam = True
        try:
            item = param.itemClass(param, 0)
            editWidget = item.makeWidget()
            hookupParamWidget(param, editWidget)
        except AttributeError as ex:
            raise ValueError(
                "Can only create EasyWidgets from parameters that have an itemClass and implement makeWidget()."
                f' Problem type: {opts["type"]}'
            )
        lbl = QtWidgets.QLabel(opts["name"])
        obj = cls([lbl, editWidget], layout)
        obj.build()
        if returnParam:
            return obj, param
        return obj


class HasEasyChild(QtWidgets.QMainWindow):
    """Provided just for type checking purposes"""

    easyChild: EasyWidget


class ImageViewer(CompositionMixin, pg.PlotWidget):
    sigMouseMoved = QtCore.Signal(object)  # ndarray(int, int) xy pos rel. to image

    def __init__(self, imgSrc: np.ndarray = None, **kwargs):
        super().__init__(**kwargs)
        self.pxColorLbl, self.mouseCoordsLbl = None, None
        """
    Set these to QLabels to have up-to-date information about the image coordinates
    under the mouse    
    """
        self.toolsEditor = params.ParamEditor(name="Region Tools")
        vb = self.getViewBox()
        self.menu: QtWidgets.QMenu = vb.menu
        self.oldVbMenu: ViewBoxMenu = vb.menu
        # Disable default menus
        self.plotItem.ctrlMenu = None
        self.sceneObj.contextMenu = None

        self.setAspectLocked(True)
        vb.invertY()

        # -----
        # IMAGE
        # -----
        self.imgItem = self.exposes(pg.ImageItem())
        self.imgItem.setZValue(-100)
        self.addItem(self.imgItem)
        if imgSrc is not None:
            self.setImage(imgSrc)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        super().mouseMoveEvent(ev)
        pos = ev.position() if hasattr(ev, "position") else ev.localPos()
        relpos = self.imgItem.mapFromScene(pos)
        xyCoord = np.array([relpos.x(), relpos.y()], dtype=int)
        if (
            self.imgItem.image is None
            or np.any(xyCoord < 0)
            or np.any(xyCoord > np.array(self.imgItem.image.shape[:2][::-1]) - 1)
        ):
            return
        imgValue = self.imgItem.image[xyCoord[1], xyCoord[0], ...]
        self.updateCursorInfo(xyCoord, imgValue)
        self.sigMouseMoved.emit(xyCoord)

    def updateCursorInfo(self, xyPos: np.ndarray, pxValue: np.ndarray):
        if pxValue is None:
            return
        if self.mouseCoordsLbl is not None:
            self.mouseCoordsLbl.setText(f"Mouse (x,y): {xyPos[0]}, {xyPos[1]}")

        if self.pxColorLbl is None:
            return
        self.pxColorLbl.setText(f"Pixel Color: {pxValue}")
        if self.imgItem.qimage is None:
            return
        imColor = self.imgItem.qimage.pixelColor(*xyPos)
        grayClr = QtGui.qGray(imColor.rgb())
        fontColor = "black" if grayClr > 127 else "white"
        self.pxColorLbl.setStyleSheet(f"background:{imColor.name()}; color:{fontColor}")

    def setImage(self, imgSrc: t.Union[FilePath, np.ndarray] = None, stripAlpha=False):
        """
        Allows the user to change the main image either from a filepath or array data.
        Files can be any format accepted by QImage -> pg.imageToArray
        Optionally strips the alpha channel from the image, if it exists (i.e. if its shape is MxNx4)
        """
        if isinstance(imgSrc, FilePath.__args__):
            # TODO: Handle alpha channel images. For now, discard that data
            qtImg = QtGui.QImage(str(imgSrc))
            nchans = qtImg.bitPlaneCount() // 8
            imgSrc = pg.imageToArray(qtImg, transpose=False)

            if nchans >= 3:
                chanOrder = [2, 1, 0]
                # Alpha is always added by imageToArray, so chop it off if necessary
                if nchans == 4:
                    chanOrder.append(3)
                imgSrc = imgSrc[..., chanOrder]
                # imageToArray creates bgr array, turn this into rgb. Also, some algorithms perform better
                # with contiguous arrays, so make sure potential views after this operation remain contiguous
                # Finally, force a copy to avoid crashing after qtImg (which owns the array) is garbage collected
            imgSrc = imgSrc.copy(order="C")
        if imgSrc is None:
            self.imgItem.clear()
        else:
            if stripAlpha and imgSrc.ndim > 2:
                imgSrc = imgSrc[:, :, :3]
            self.imgItem.setImage(imgSrc)

    def widgetContainer(self, asMainWin=True, showTools=True, **kwargs):
        """
        Though this is a PlotWidget class, it has a lot of widget children (toolsEditor group, buttons) that are
        not visible when spawning the widget. This is a convenience method that creates a new, outer widget
        from all teh graphical elements of an EditableImage.

        :param asMainWin: Whether to return a QMainWindow or QWidget
        :param showTools: If `showMainWin` is True, this determines whether to show the tools
          editor with the window
        :param kwargs: Passed to either EasyWidget.buildMainWin or EasyWidget.BuildWidget,
          depending on the value of `asMainWin`
        """
        if asMainWin:
            wid = EasyWidget.buildMainWin(self._widgetContainerChildren(), **kwargs)
            self.mouseCoordsLbl = QtWidgets.QLabel()
            self.pxColorLbl = QtWidgets.QLabel()
            wid.statusBar().addWidget(self.mouseCoordsLbl)
            wid.statusBar().addWidget(self.pxColorLbl)
            wid.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.toolsEditor)
            if showTools:
                self.toolsEditor.show()
        else:
            wid = EasyWidget.buildWidget(self._widgetContainerChildren(), **kwargs)
        return wid

    def showAndExec(self):
        win = self.widgetContainer(True)
        QtCore.QTimer.singleShot(0, win.showMaximized)
        QtCore.QCoreApplication.instance().exec_()

    def show_exec(self):
        warn("'show_exec' is deprecated, please use 'showAndExec'", DeprecationWarning)
        return self.showAndExec()

    def _widgetContainerChildren(self):
        """
        Returns the children that should be added to the container when widgetContainer()
        is called
        """
        return [self]


class CompositorItemSample(ItemSample):
    def paint(self, p: QtGui.QPainter, *args):
        opts = self.item.opts

        if opts.get("antialias"):
            p.setRenderHint(p.Antialiasing)
        symbol = opts.get("symbol", None)
        p.translate(0, 14)
        drawSymbol(
            p, symbol, opts["size"], pg.mkPen(opts["pen"]), pg.mkBrush(opts["brush"])
        )


class CompositorLegend(pg.LegendItem):
    def paint(self, p: QtGui.QPainter, *args):
        br = self.boundingRect()
        p.setPen(self.opts["pen"])
        p.setBrush(self.opts["brush"])
        p.drawRoundedRect(br, 5, 5)


class MaskCompositor(ImageViewer):
    _cachedCmapLimits = None

    def __init__(self, img: np.ndarray = None):
        super().__init__()
        # -----
        # Create properties
        # -----
        self.masksParam = getParamChild(self.toolsEditor.params, "Overlays")
        if self._cachedCmapLimits is None:
            # Set at class level to cache for new instances too
            type(self)._cachedCmapLimits = listAllPgColormaps()

        self.legend = CompositorLegend(
            offset=(5, 5), horSpacing=5, brush="ccce", pen="k"
        )
        self.recordDf = pd.DataFrame(
            columns=["name", "item", "opacity", "isMask"]
        ).set_index("name")
        # Initialized in clearOverlays and updateLabelMap. Given here to avoid intellisense warnings
        self.inUseLabelValues = (
            self.scatterSer
        ) = self.backgroundValues = self.labelToNameMapping = None
        self.updateLabelMap()
        self.legendFontArgs = {"size": "11pt", "color": "k", "bold": True}
        self.curZ = 2

        # -----
        # Configure relationships
        # -----
        self.legend.setParentItem(self.plotItem)
        self.viewbox: pg.ViewBox = self.getViewBox()

        self.allVisible = True
        # for ax in 'left', 'bottom', 'right', 'top':
        #   self.mainImg.plotItem.hideAxis(ax)
        # self.mainImg.setContentsMargins(0, 0, 0, 0)
        def newFmt(name):
            if name.startswith("set"):
                name = name.replace("set", "")
            name = pascalCaseToTitle(name)
            return name

        with nameFormatter.set(newFmt):
            self.propertiesProc = self.toolsEditor.registerFunc(
                self.setOverlayProperties,
                runOpts=params.RunOpts.ON_CHANGED,
                colormap=dict(limits=self._cachedCmapLimits),
            )
            self.toolsEditor.registerFunc(self.save)
            self.toolsEditor.registerFunc(
                lambda: self.imgItem.setVisible(not self.imgItem.isVisible()),
                name="Toggle Image Visible",
            )
            self.toolsEditor.registerFunc(
                lambda: self.legend.setVisible(not self.legend.isVisible()),
                name="Toggle Legend Visible",
            )
            self.toolsEditor.registerFunc(self.toggleAllVisible, namePath=("Overlays",))
        if img is not None:
            self.setImage(img)
        self.clearOverlays()

    @staticmethod
    def _createLabelToNameMapping(data=None):
        """Helper method to ensure proper dtypes when making a legend series. Helps avoid pitfalls with empty data, etc."""
        if data is None:
            data = []
        ser = pd.Series(data, dtype=str)
        ser.index = ser.index.astype("int64", copy=False)
        return ser

    def _addItemCtrls(self, record: pd.Series):
        item = record["item"]

        def maskOpts(_, visible=True):
            item.setVisible(visible)

        newParam = getParamChild(
            self.masksParam, chOpts={"name": record.name, "type": "bool", "value": True}
        )
        newParam.sigValueChanged.connect(maskOpts)

    def setBaseImage(self, baseImg: np.ndarray, clearOverlays=True):
        # self.winSz = baseImg.shape[:2][::-1]
        # self.viewbox.setRange(
        #   xRange=[0, imgItem.shape[1]], yRange=[0, imgItem.shape[0]], padding=0
        # )
        self.setImage(baseImg)
        # self.refreshWinContents()
        if clearOverlays:
            self.clearOverlays()

    def setImage(self, *args, **kwargs):
        super().setImage(*args, **kwargs)
        self._updateLegendPos()

    def _addRecord(self, rec: pd.Series, update=True):
        self.recordDf = pd.concat([self.recordDf, rec.to_frame().T], axis=0)
        self.curZ += 1

        self._addItemCtrls(rec)

        if update:
            self._updateGraphics()

    def addImageItem(self, item: pg.ImageItem, **kwargs):
        kwargs.setdefault("opacity", -1)
        name = self._getUniqueName(kwargs.pop("name", None))
        update = kwargs.pop("update", True)
        kwargs.setdefault("isMask", False)
        newRecord = dict(item=item, **kwargs)
        item.setZValue(self.curZ + 1)
        self.viewbox.addItem(item)

        rec = pd.Series(newRecord, name=name)
        self._addRecord(rec, update)

    def _getUniqueName(self, baseName: str = None):
        if baseName is None:
            baseName = "[No Name]"
        ii = 2
        name = baseName
        while name in self.recordDf.index:
            name = f"{baseName} {ii}"
            ii += 1
        return name

    def addLabelMask(
        self,
        labelMask: np.ndarray,
        name=None,
        clearOverlays=False,
        fullLabelMapInLegend=False,
        **overlayKwargs,
    ):
        """
        Splits a label mask into its constituent labels and adds a mask for each unique label.

        :param labelMask: Grayscale label mask of integers
        :param name: Name to identify this mask in the property editor
        :param clearOverlays: If *True*, `clearOverlays` will be called before adding this item. This is useful
          if only one mask is viewed at a time
        :param fullLabelMapInLegend: See ``updateLegendEntries`` -- this parameter is passed during legend creation
        :param overlayKwargs: Keyword arguments passed to setOverlayProperties
        """
        if clearOverlays and len(self.recordDf):
            # Reuse item if possible
            item = self._reuseLastOverlay(labelMask, name)
        else:
            item = None
        maskValues = np.unique(labelMask.ravel())
        # Booleans don't mix well with int series indexing/logic
        # Floats are completely wonky
        if np.issubdtype(maskValues.dtype, np.bool_):
            maskValues = maskValues.astype("uint8")
        elif not np.issubdtype(maskValues.dtype, np.integer):
            raise ValueError(
                f'Overlays can only be created using integer dtypes. Encountered "{maskValues.dtype}"'
            )

        self.inUseLabelValues = np.union1d(self.inUseLabelValues, maskValues)
        self.updateLegendEntries(useFullLabelMap=fullLabelMapInLegend)
        if item is None:
            self.addImageItem(
                pg.ImageItem(labelMask),
                name=name,
                isMask=True,
                opacity=-1,
                update=False,
            )
        self.propertiesProc.run(**overlayKwargs)

    def _reuseLastOverlay(self, newImageData=None, newName=None, isMask=True):
        """
        When a set of images must be overlaid separately, it is more efficient to reuse an
        image item compared to constantly adding and removing them from a scene.
        Assumes at least one record is already present in ``self.recordDf``
        """
        self.clearOverlays(self.recordDf.index[:-1])
        # Use two steps to update name so conflicts are avoided
        self.recordDf.index = [None]
        self.recordDf.index = [self._getUniqueName(newName)]
        rec = self.recordDf.iloc[-1]
        rec["isMask"] = isMask
        item = rec["item"]
        item.setImage(newImageData)
        return item

    def setLegendFontStyle(self, startItemIdx=0, **lblTxtArgs):
        for item in self.legend.items[startItemIdx:]:
            for single_item in item:
                if isinstance(single_item, pg.LabelItem):
                    single_item.setText(single_item.text, **lblTxtArgs)

    def updateLegendEntries(self, useFullLabelMap=False, updateOverlays=False):
        """
        :param useFullLabelMap: If *True*, guarantees that every entry in the label->name mapping will be present
          in the legend.
        :param updateOverlays: If *True*, the image overlay properties will be refereshed
        """
        if useFullLabelMap:
            labels = np.union1d(self.inUseLabelValues, self.labelToNameMapping.index)
        else:
            labels = self.inUseLabelValues
        labels = np.setdiff1d(labels, self.backgroundValues)
        names = self.labelToNameMapping.reindex(labels)
        needsEntry = names.isna()
        names[needsEntry] = names.index[needsEntry].map(str)
        self.legend.clear()
        self.scatterSer = pd.Series(
            [None] * len(names), index=names.index, dtype=object
        )
        # Make sure alpha is not carried over
        for value, name in names.iteritems():
            scat = pg.ScatterPlotItem(symbol="s", width=5)
            self.legend.addItem(CompositorItemSample(scat), name=name)
            self.scatterSer.at[value] = scat
        if updateOverlays:
            self.propertiesProc.run()

    def updateLabelMap(
        self,
        labelMap: dict | pd.Series = None,
        backgroundValues=0,
        updateOverlays=False,
    ):
        """
        :param labelMap: Series or dict-like with integer key and string value. Gives a legend name to each label in
          the image. Unspecified labels will be named by their numeric value, e.g. 34 will be '34'. Note that this
          will update the global legend, meaning if {10 -> 'test'} is a legend entry, it will overwrite the old
          legend value for 10.
        :param backgroundValues: Represents label mask values that should be transparent in the overlay
        :param updateOverlays: If *True*, overlay graphics will be refreshed to reflect these updates. Keep *False* if
          several updates will happen in sequence.
        """
        if labelMap is None:
            labelMap = {}
        if np.isscalar(backgroundValues):
            backgroundValues = [backgroundValues]
        self.backgroundValues = np.array(backgroundValues)
        self.labelToNameMapping = self._createLabelToNameMapping(labelMap)
        if updateOverlays:
            self._updateGraphics()

    def setOverlayProperties(
        self, colormap="magma", opacity=0.6, fullLabelMapColors=False
    ):
        """
        Sets overlay properties
        :param colormap:
          pType: popuplineeditor
        :param opacity:
          limits: [0,1]
          step: 0.1
        :param fullLabelMapColors: If *True*, enough colors will be generated for all labels in
          ``self.labelToNameMapping``. If *False*, only enough colors will be generated for the labels in the
          added masks.
          ignore: True
        """
        maskIdxs = self.recordDf["isMask"].to_numpy(bool)
        cmap = getAnyPgColormap(colormap)
        labelValues = self.scatterSer.index.values
        if fullLabelMapColors:
            labelValues = np.union1d(labelValues, self.labelToNameMapping.index.values)
        if not len(labelValues):
            pass  # return
        if cmap is None:
            raise ValueError(f"Invalid colormap: {colormap}")
        colors = cmap.getLookupTable(nPts=len(labelValues), alpha=True)
        colors[:, -1] = opacity * 255
        # If a labelmap has entries, try to scale the colormap to contain all possibilities
        numEntries = (
            max(
                np.max(labelValues, initial=-1),
                np.max(self.labelToNameMapping.index.values, initial=-1),
            )
            + 1
        )
        lut = np.zeros((numEntries, 4), dtype="uint8")
        lut[labelValues] = colors
        bgValsInLut = self.backgroundValues[self.backgroundValues < len(lut)]
        lut[bgValsInLut] = 0
        for idx, scat in self.scatterSer.iteritems():
            # Make sure alpha is not carried over
            color = lut[idx, :-1]
            brush, pen = pg.mkBrush(color), pg.mkPen(color)
            scat.setData(symbol="s", brush=brush, pen=pen, width=5)
        for _, maskRec in self.recordDf[maskIdxs].iterrows():
            itemOpacity = maskRec["opacity"]
            if itemOpacity < 0:
                itemOpacity = opacity
            maskRec["item"].setOpts(
                lut=lut, opacity=itemOpacity, levels=[0, numEntries - 1]
            )
        # Handle non-mask items who still want controlled opacity
        for _, rec in self.recordDf[
            (~maskIdxs) & self.recordDf["opacity"] < 0
        ].iterrows():
            rec["item"].setOpts(opacity=opacity)
        self.setLegendFontStyle(**self.legendFontArgs)
        self.legend.update()

        # Handle all non-mask items now
        for name, remainingRec in self.recordDf[~maskIdxs].iterrows():
            curOpacity = remainingRec["opacity"]
            if curOpacity < 0:
                curOpacity = opacity
            remainingRec["item"].setOpacity(curOpacity)

    def _updateLegendPos(self):
        imPos = self.imgItem.mapToScene(self.imgItem.pos())
        self.legend.autoAnchor(imPos)

    def _updateGraphics(self):
        self.propertiesProc.run()

    def clearOverlays(self, clearIdxs=None):
        """
        Clears image item overlays by index. If No index is specified, all overlays are removed
        :param clearIdxs: Indexes of overlays to remove
        ignore: True
        """
        if clearIdxs is None:
            clearIdxs = self.recordDf.index
        for imgItem in self.recordDf.loc[clearIdxs, "item"]:
            self.viewbox.removeItem(imgItem)
        keepIdxs = np.setdiff1d(self.recordDf.index, clearIdxs)
        self.recordDf: pd.DataFrame = self.recordDf.loc[keepIdxs].copy()
        self.inUseLabelValues = np.array([], "int64")
        self.updateLegendEntries()
        overlayParam = self.toolsEditor.params.child("Overlays")

        for idx in clearIdxs:
            overlayParam.child(idx).remove()

    def toggleAllVisible(self):
        for param in self.masksParam:
            if param.type() == "bool":
                param.setValue(not self.allVisible)
        self.allVisible = not self.allVisible

    def save(
        self,
        saveFile: FilePath = "",
        cropToViewbox=False,
        toClipboard=False,
        floatLegend=False,
    ):
        """
        :param saveFile:
          helpText: Save destination. If blank, no file is created.
          existing: False
          pType: filepicker
        :param toClipboard: Whether to copy to clipboard
        :param cropToViewbox: Whether to only save the visible portion of the image
        :param floatLegend: Whether to ancor the legend in the top-left corner (if *False*) or
          put it exactly where it is positioned currently (if *True*). In the latter case, it may not appear if out of view
          and `cropToViewbox` is *True*.
        """
        if self.imgItem.isVisible():
            saveImg = self.imgItem.getPixmap()
        else:
            saveImg = QtGui.QPixmap(*self.imgItem.image.shape[:2][::-1])
        painter = QtGui.QPainter(saveImg)

        visibleMasks = [p.name() for p in paramsFlattened(self.masksParam) if p.value()]
        for name, item in self.recordDf["item"].iteritems():
            if name in visibleMasks:
                painter.setOpacity(item.opacity())
                item.paint(painter)
        painter.setOpacity(1.0)

        if cropToViewbox:
            maxBnd = np.array(self.image.shape[:2][::-1]).reshape(-1, 1) - 1
            vRange = np.array(self.viewbox.viewRange()).astype(int)
            vRange = np.clip(vRange, 0, maxBnd)
            # Convert range to topleft->bottomright
            pts = QtCore.QPoint(*vRange[:, 0]), QtCore.QPoint(*vRange[:, 1])
            # Qt doesn't do so well overwriting the original reference
            origRef = saveImg
            saveImg = origRef.copy(QtCore.QRect(*pts))
            painter.end()
            painter = QtGui.QPainter(saveImg)
        if self.legend.isVisible():
            # Wait to paint legend until here in case cropping is active
            self._paintLegend(painter, floatLegend)

        if toClipboard:
            QtWidgets.QApplication.clipboard().setImage(saveImg.toImage())

        saveFile = str(saveFile)
        if saveFile and not saveImg.save(str(saveFile)):
            warn("Image compositor save failed", UserWarning)
        return saveImg

    def _paintLegend(self, painter: QtGui.QPainter, floatLegend=False):
        oldPos = self.legend.pos()
        try:
            exportScene = GraphicsScene(parent=None)
            oldScale = max(np.clip(0.5 / np.array(self.imgItem.pixelSize()), 1, np.inf))
            exportScene.addItem(self.legend)
            self.legend.setScale(oldScale)
            # Legend does not scale itself, handle this
            painter.save()
            if floatLegend:
                viewPos = self.viewbox.viewRect()
                viewX = max(viewPos.x(), 0)
                viewY = max(viewPos.y(), 0)
                imPos = self.legend.mapRectToItem(self.imgItem, self.legend.rect())
                painter.translate(int(imPos.x() - viewX), int(imPos.y() - viewY))
            exportScene.render(painter)
            self.legend.setScale(1 / oldScale)
            painter.restore()
        finally:
            self.legend.setParentItem(self.plotItem)
            self.legend.autoAnchor(oldPos, relative=False)

    def __getstate__(self):
        ret = dict(
            image=self.imgItem.image,
            legendVisible=self.legend.isVisible(),
        )
        if len(self.recordDf):
            ret["recordDf"] = self.recordDf

    def __setstate__(self, state):
        self.__init__(state["image"])
        self.legend.setVisible(state["legendVisible"])
        if "recordDf" in state:
            for _, rec in state["recordDf"].iteritems():
                self._addRecord(rec, False)
            self._updateGraphics()


class PandasTableModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    sigDataChanged = QtCore.Signal(object)
    defaultEmitDict = {
        "deleted": np.array([]),
        "changed": np.array([]),
        "added": np.array([]),
    }

    # Will be set in 'changeDefaultRows'
    df: pd.DataFrame
    _defaultSer: pd.Series

    def __init__(self, defaultSer: pd.Series, parent=None):
        super().__init__(parent)
        self.df = pd.DataFrame()
        self.changeDefaultRows(defaultSer)
        self._nextRowId = 0

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):
        return self.df.shape[1]

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            value = self.df.iloc[index.row(), index.column()]
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(value)
            elif role == QtCore.Qt.ItemDataRole.EditRole:
                return value
        return None

    def setData(
        self,
        index: QtCore.QModelIndex,
        value: t.Any,
        role: int = QtCore.Qt.ItemDataRole,
    ) -> bool:
        super().setData(index, role)
        row = index.row()
        col = index.column()
        oldVal = self.df.iat[row, col]
        # Try-catch for case of numpy arrays
        noChange = oldVal == value
        try:
            if noChange:
                return True
        except ValueError:
            # Happens with array comparison
            pass
        self.df.iat[row, col] = value
        self.sigDataChanged.emit()
        return True

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if (
            orientation == QtCore.Qt.Orientation.Horizontal
            and role == QtCore.Qt.ItemDataRole.DisplayRole
        ):
            return self.df.columns[section]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable

    def addDfRows(
        self, rowData: pd.DataFrame, addType=PrjEnums.ADD_TYPE_NEW, emitChange=True
    ):
        toEmit = self.defaultEmitDict.copy()
        if addType == PrjEnums.ADD_TYPE_NEW:
            # Treat all comps as new -> set their IDs to guaranteed new values
            newIds = np.arange(
                self._nextRowId, self._nextRowId + len(rowData), dtype=int
            )
            rowData.set_index(newIds, inplace=True, verify_integrity=False)
            # For new data without all columns, add missing values to ensure they're correctly filled
            if np.setdiff1d(rowData.columns, self.df.columns).size > 0:
                rowData = self.makeDefaultDfRows(len(rowData), rowData)
        else:
            # Merge may have been performed with new comps (id -1) mixed in
            needsUpdatedId = rowData.index == -1
            newIds = np.arange(
                self._nextRowId, self._nextRowId + np.sum(needsUpdatedId), dtype=int
            )
            rowData.index[needsUpdatedId] = newIds

        # Merge existing IDs and add new ones
        changedIdxs = np.isin(rowData.index, self.df.index, assume_unique=True)
        changedIds = rowData.index[changedIdxs]
        addedIds = rowData.index[~changedIdxs]

        # Signal to table that rows should change
        self.layoutAboutToBeChanged.emit()
        # Ensure indices overlap with the components these are replacing
        self.df.update(rowData)
        toEmit["changed"] = changedIds

        # Finally, add new comps
        compsToAdd = rowData.loc[addedIds]
        self.df = pd.concat((self.df, compsToAdd), sort=False)
        toEmit["added"] = addedIds

        # Retain type information
        self._coerceDfTypes()

        self.layoutChanged.emit()

        self._nextRowId = np.max(self.df.index.to_numpy(), initial=-1) + 1

        if emitChange:
            self.sigDataChanged.emit(toEmit)
        return toEmit

    def removeDfRows(self, idsToRemove: t.Sequence[int] = None, emitChange=True):
        if idsToRemove is None:
            idsToRemove = self.df.index
        toEmit = self.defaultEmitDict.copy()
        # Generate ID list
        existingCompIds = self.df.index
        idsToRemove = np.asarray(idsToRemove)

        # Do nothing for IDs not actually in the existing list
        idsActuallyRemoved = np.isin(idsToRemove, existingCompIds, assume_unique=True)
        if len(idsActuallyRemoved) == 0:
            return toEmit
        idsToRemove = idsToRemove[idsActuallyRemoved]

        tfKeepIdx = np.isin(
            existingCompIds, idsToRemove, assume_unique=True, invert=True
        )

        # Reset manager's component list
        self.layoutAboutToBeChanged.emit()
        self.df = self.df.iloc[tfKeepIdx, :]
        self.layoutChanged.emit()

        # Preserve type information after change
        self._coerceDfTypes()

        # Determine next ID for new components
        self._nextRowId = 0
        if np.any(tfKeepIdx):
            self._nextRowId = np.max(existingCompIds[tfKeepIdx].to_numpy()) + 1

        # Reflect these changes to the component list
        toEmit["deleted"] = idsToRemove
        if emitChange:
            self.sigDataChanged.emit(toEmit)

    def makeDefaultDfRows(self, numRows=1, initData: pd.DataFrame = None):
        """
        Create a dummy table populated with default values from the class default pd.Series. If `initData` is provided, it
        must have numRows entries and correspond to columns from the default series. these columns will be overridden by
        the init data.
        """
        if numRows == 0:
            return pd.DataFrame(columns=self._defaultSer.index)
        outDf = pd.DataFrame([self._defaultSer] * numRows)
        if initData is not None:
            outDf.update(initData.set_index(outDf.index))
        return outDf

    def changeDefaultRows(self, defaultSer: pd.Series):
        self.beginResetModel()
        self._defaultSer = defaultSer
        self.removeDfRows(self.df.index)
        self.df = self.makeDefaultDfRows(0)
        self.endResetModel()

    def _coerceDfTypes(self):
        """
        Pandas currently has a bug where datatypes are not preserved after update operations.
        Current workaround is to coerce all types to their original values after each operation
        """
        for ii, col in enumerate(self.df.columns):
            idealType = type(self._defaultSer[col])
            if not np.issubdtype(self.df.dtypes[ii], idealType):
                try:
                    self.df[col] = self.df[col].astype(idealType)
                except (TypeError, ValueError):
                    continue


class QtAppHandler(logging.Handler):
    _weakWin: weakref.ReferenceType = None

    def __init__(
        self, level, win: QtWidgets.QMainWindow = None, exceptionsOnly=False
    ) -> None:
        super().__init__(level)
        self.attachWinRef(win)
        self.exceptionsOnly = exceptionsOnly

    def attachWinRef(self, win=None):
        if win is not None:
            win = weakref.ref(win)
        self._weakWin = win

    def getWin(self) -> t.Optional[QtWidgets.QMainWindow]:
        if self._weakWin is None:
            return None
        return self._weakWin()


class DialogHandler(QtAppHandler):
    def emit(self, record: logging.LogRecord):
        if record.exc_info:
            msg = html.escape(str(record.exc_info[1]))
            excStr = "".join(format_exception(*record.exc_info))
            detailed = html.escape(excStr)
        else:
            msg = super().format(record)
            detailed = getattr(record, "detailed", msg)
        dlgType = "Critical" if record.levelno == logging.CRITICAL else "Information"

        dlg = ScrollableMessageDialog(self.getWin(), dlgType, msg, detailed)

        def doExec():
            dlg.exec()

        # Using function instead of directly connecting to dlg.exec keeps garbage from being collected just long enough
        QtCore.QTimer.singleShot(0, doExec)

    def filter(self, record: logging.LogRecord):
        """Optionally only activates this handler if the message came from an exception"""
        if not self.exceptionsOnly:
            return super().filter(record)
        try:
            return len(record.exc_info) > 1
        except Exception:
            return False


class TimedMessageHandler(QtAppHandler):
    def __init__(
        self, *args, defaultMsgtimeout_ms=3000, maxLevel=None, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.defaultMsgTimeout = defaultMsgtimeout_ms
        if maxLevel is None:
            maxLevel = sys.maxsize
        self.maxLevel = maxLevel

    def emit(self, record: logging.LogRecord):
        win = self.getWin()
        if win is None:
            return
        if hasattr(record, "msgTimeout"):
            msgTimeout = record.msgTimeout
        else:
            msgTimeout = self.defaultMsgTimeout
        self.makeNotification(self.format(record), msgTimeout)

    def filter(self, record: logging.LogRecord):
        return record.levelno <= self.maxLevel and logging.Handler.filter(self, record)

    def makeNotification(self, msg: str, timeout_ms: int = None):
        raise NotImplementedError


class StatusBarHandler(TimedMessageHandler):
    def makeNotification(self, msg: str, timeout_ms: int = None):
        self.getWin().statusBar().showMessage(msg, timeout_ms)


class FadeNotifyHandler(TimedMessageHandler):
    updateFps = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If references aren't kept to labels, they will caused wrapped c++ deletion errors
        # List instead of single ref since multiple messages can exist at once
        # Dict to also associate animations with their window
        self.msgRefs = {}

    def makeNotification(self, msg: str, timeout_ms: int = None):
        """
        Creates a fading green dialog that shows the message and disappears after timeout
        """
        style = """\
    QLabel {
      background-color: #0f0;
      border: 1px solid #000;
      color: #000;
    };
    """
        fadeMsg = QtWidgets.QLabel(msg, self.getWin())
        fadeMsg.setStyleSheet(style)
        # For some reason, width doesn't set properly here
        fadeMsg.setFixedWidth(fadeMsg.sizeHint().width())
        fadeMsg.setAlignment(QtCore.Qt.AlignCenter)
        fadeMsg.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        parent: QtWidgets.QMainWindow = self.getWin()
        if parent is not None:
            metrics = fadeMsg.fontMetrics()
            padding = (parent.width() - metrics.width(msg)) // 2
            msgX = padding
            # Make sure multiple messages don't overlap
            msgY = int(0.05 * parent.height())
            msgY += self.getUniqueLblOffset(msgY)
            fadeMsg.move(msgX, msgY)
        anim = self.makeAnimation(fadeMsg, timeout_ms)
        # 10 fps
        anim.start(1000 // self.updateFps)
        fadeMsg.show()

    def getUniqueLblOffset(self, constHeight):
        allYPos = np.array([l.pos().y() - constHeight for l in self.msgRefs])
        if not len(allYPos):
            return 0
        height = next(iter(self.msgRefs)).height()
        offset = 0
        recalc = True
        while recalc:
            offset += 0.8 * height
            recalc = np.min(np.abs(allYPos - offset)) < 0.01
        return offset

    def closeMsgWidget(self, msgWidget):
        """
        Closes the specified messages and deletes corresponding references
        """
        msgWidget.hide()
        msgWidget.deleteLater()
        self.msgRefs[msgWidget].deleteLater()
        del self.msgRefs[msgWidget]

    def makeAnimation(self, widget, timeout_ms):
        """
        The default method of using a PropertyAnimation doesn't repaint the widget, so do it a quick and dirty way
        using timers manually
        """

        def changeOpacity():
            for opacity in np.linspace(1, 0, int(timeout_ms / 1000 * self.updateFps)):
                effect.setOpacity(opacity)
                # widget.update()
                yield
            # Animation done, wait one tick to prevent overlaps
            yield
            self.closeMsgWidget(widget)

        # Don't start right away
        effect = QtWidgets.QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = timedExec(changeOpacity, interval_ms=0)
        self.msgRefs[widget] = anim
        return anim
