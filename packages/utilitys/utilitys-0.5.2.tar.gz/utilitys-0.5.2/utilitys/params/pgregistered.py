from __future__ import annotations

import warnings
from pathlib import Path
from typing import Optional

import numpy as np
from pyqtgraph.Qt import QtGui, QtWidgets, QtCore
from pyqtgraph.parametertree import parameterTypes, Parameter, ParameterItem
from pyqtgraph.parametertree.Parameter import PARAM_TYPES
from pyqtgraph.parametertree.parameterTypes import (
    ActionParameterItem,
    ActionParameter,
    TextParameterItem,
    TextParameter,
    WidgetParameterItem,
    ChecklistParameter,
)

from .prjparam import PrjParam
from .shortcut import ShortcutsEditor
from .. import fns
from ..fns import clsNameOrGroup, paramsFlattened, popupFilePicker
from ..widgets import PopupLineEditor, ButtonCollection


class MonkeyPatchedTextParameterItem(TextParameterItem):
    def makeWidget(self):
        textBox: QtWidgets.QTextEdit = super().makeWidget()
        textBox.setTabChangesFocus(True)
        return textBox


# Monkey patch pyqtgraph text box to allow tab changing focus
TextParameter.itemClass = MonkeyPatchedTextParameterItem


class ParamDialog(QtWidgets.QDialog):
    def __init__(self, param: Parameter, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.param = param
        self.tree = fns.flexibleParamTree(param)
        self.saveChanges = False

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tree)

        okBtn = QtWidgets.QPushButton("Ok")
        cancelBtn = QtWidgets.QPushButton("Cancel")
        btnLay = QtWidgets.QHBoxLayout()
        btnLay.addWidget(okBtn)
        btnLay.addWidget(cancelBtn)
        layout.addLayout(btnLay)

        def okClicked():
            self.saveChanges = True
            self.accept()

        def cancelClicked():
            self.saveChanges = False
            self.reject()

        okBtn.clicked.connect(okClicked)
        cancelBtn.clicked.connect(cancelClicked)


class PgPopupDelegate(QtWidgets.QStyledItemDelegate):
    """
    For pyqtgraph-registered parameter types that don't define an itemClass with `makeWidget`, this
    popup delegate can be used instead which creates a popout parameter tree.
    """

    def __init__(self, paramDict: dict, parent=None):
        super().__init__(parent)
        paramDict.setdefault("name", paramDict["type"])
        self.param = Parameter.create(**paramDict)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        self.param.setValue(index.data(QtCore.Qt.ItemDataRole.EditRole))
        editor = ParamDialog(self.param)
        editor.show()
        editor.resize(editor.width() + 50, editor.height() + 30)

        return editor

    def setModelData(
        self,
        editor: QtWidgets.QWidget,
        model: QtCore.QAbstractTableModel,
        index: QtCore.QModelIndex,
    ):
        if editor.saveChanges:
            model.setData(index, editor.param.value())

    def setEditorData(self, editor: QtWidgets.QWidget, index):
        value = index.data(QtCore.Qt.ItemDataRole.EditRole)
        self.param.setValue(value)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        return


class PgParamDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, paramDict: dict, parent=None):
        super().__init__(parent)
        errMsg = (
            f"{self.__class__} can only create parameter editors from registered pg widgets whose items subclass"
            f' "WidgetParameterItem" and are in pyqtgraph\'s *PARAM_TYPES*.\nThese requirements are not met for type'
            f' "{paramDict["type"]}"'
        )

        if paramDict["type"] not in PARAM_TYPES:
            raise TypeError(errMsg)
        paramDict.update(name="dummy")
        self.param = param = Parameter.create(**paramDict)
        item = param.makeTreeItem(0)
        if isinstance(item, WidgetParameterItem):
            self.item = item
        else:
            raise TypeError(errMsg)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        # TODO: Deal with params that go out of scope before yielding a value
        editor = self.item.makeWidget()
        editor.setParent(parent)
        editor.setMaximumSize(option.rect.width(), option.rect.height())
        return editor

    def setModelData(
        self,
        editor: QtWidgets.QWidget,
        model: QtCore.QAbstractTableModel,
        index: QtCore.QModelIndex,
    ):
        model.setData(index, editor.value())

    def setEditorData(self, editor: QtWidgets.QWidget, index):
        value = index.data(QtCore.Qt.ItemDataRole.EditRole)
        editor.setValue(value)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        editor.setGeometry(option.rect)


class KeySequenceParameterItem(parameterTypes.WidgetParameterItem):
    """
    Class for creating custom shortcuts. Must be made here since pyqtgraph doesn't
    provide an implementation.
    """

    def makeWidget(self):
        item = QtWidgets.QKeySequenceEdit()

        item.sigChanged = item.editingFinished
        item.value = lambda: item.keySequence().toString()

        def setter(val: QtGui.QKeySequence):
            if val is None or len(val) == 0:
                item.clear()
            else:
                item.setKeySequence(val)

        item.setValue = setter
        self.param.seqEdit = item

        return item

    def updateDisplayLabel(self, value=None):
        # Make sure the key sequence is human readable
        self.displayLabel.setText(self.widget.keySequence().toString())

    # def contextMenuEvent(self, ev: QtGui.QContextMenuEvent):
    #   menu = self.contextMenu
    #   delAct = QtGui.QAction('Set Blank')
    #   delAct.triggered.connect(lambda: self.widget.setValue(''))
    #   menu.addAction(delAct)
    #   menu.exec(ev.globalPos())


class _Global:
    pass


class KeySequenceParameter(Parameter):
    itemClass = KeySequenceParameterItem


class ShortcutParameterItem(ActionParameterItem):
    def __init__(self, param, depth):
        # Force set title since this will get nullified on changing the button parent for some
        # reason
        super().__init__(param, depth)
        btn: QtWidgets.QPushButton = self.button
        self.setText(0, "")
        owner = param.opts.get("ownerObj", _Global)
        # Add things like icon and help text
        prjOpts = PrjParam(**param.opts)
        ButtonCollection.createBtn(
            prjOpts, baseBtn=self.button, namePath=(clsNameOrGroup(owner),)
        )

    def _postInit_(self, shcParam: Parameter):
        """
        Exists purely to assist shortcutWithKeySeq in grabbing the created shortcut parameter and placing it next to
        the button instead of in the shortcuts editor
        """
        pass


class ShortcutParameter(ActionParameter):
    itemClass = ShortcutParameterItem
    REGISTRY: Optional[ShortcutsEditor] = None

    @classmethod
    def setRegistry(
        cls, shortcutsRegistry: ShortcutsEditor = None, createIfNone=False, **createOpts
    ):
        if cls.REGISTRY:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                for param in paramsFlattened(cls.REGISTRY.params):
                    cls.REGISTRY.deleteShortcut(
                        PrjParam(param.name(), param.defaultValue())
                    )
        if createIfNone and shortcutsRegistry is None:
            shortcutsRegistry = ShortcutsEditor(**createOpts)
        cls.REGISTRY = shortcutsRegistry
        return shortcutsRegistry


class ShortcutKeySeqParameterItem(ShortcutParameterItem):
    def _postInit_(self, shcParam: Parameter):
        shcParam.remove()
        self.keySeqEdit: KeySequenceParameterItem = shcParam.makeTreeItem(self.depth)

        # Make sure that when a parameter is removed, the shortcut is also deactivated. Since the key sequence was stolen
        # from the shortcut editor, it must be addressed here
        def onRemove():
            shcParam.setValue("")
            shcParam.remove()

        self.param.sigRemoved.connect(lambda: onRemove())
        self.layout.addWidget(self.keySeqEdit.widget)


class ShortcutKeySeqParameter(ActionParameter):
    itemClass = ShortcutKeySeqParameterItem

    def __init__(self, **opts):
        # TODO: Find way to get shortcuts working well with general shortcut editor.
        #  for now, just make sure no shortcuts are registered
        opts.pop("value", None)
        super().__init__(**opts)
        self.isActivateConnected = False


class PopupLineEditorParameterItem(parameterTypes.WidgetParameterItem):
    def __init__(self, param, depth):
        strings = param.opts.get("limits", [])
        self.model = QtCore.QStringListModel(strings)
        param.sigLimitsChanged.connect(
            lambda _param, limits: self.model.setStringList(limits)
        )
        super().__init__(param, depth)

    def makeWidget(self):
        opts = self.param.opts
        editor = PopupLineEditor(
            model=self.model,
            clearOnComplete=False,
            forceMatch=opts.get("forceMatch", True),
            validateCase=opts.get("validateCase", False),
        )
        editor.setValue = editor.setText
        editor.value = editor.text
        editor.sigChanged = editor.editingFinished
        return editor

    def widgetEventFilter(self, obj, ev):
        # Prevent tab from leaving widget
        return False


class PopupLineEditorParameter(Parameter):
    itemClass = PopupLineEditorParameterItem


class ProcGroupParameterItem(parameterTypes.GroupParameterItem):
    def __init__(self, param, depth):
        self.enabledFontMap = None
        super().__init__(param, depth)

    def _mkFontMap(self):
        if self.enabledFontMap:
            return
        allowDisable = self.param.opts["process"].allowDisable
        if allowDisable:
            enabledFont = self.font(0)
        else:
            enabledFont = QtGui.QFont()
            enabledFont.setBold(False)

        disableFont = QtGui.QFont()
        disableFont.setStrikeOut(True)
        self.enabledFontMap = {True: enabledFont, False: disableFont}

    def optsChanged(self, param, opts):
        proc = param.opts["process"]
        if "enabled" in opts:
            enabled = opts["enabled"]
            if proc.allowDisable:
                # Bypass subclass to prevent early short-circuit
                if enabled:
                    super().setData(
                        0,
                        QtCore.Qt.ItemDataRole.CheckStateRole,
                        QtCore.Qt.CheckState.Checked,
                    )
                else:
                    super().setData(
                        0,
                        QtCore.Qt.ItemDataRole.CheckStateRole,
                        QtCore.Qt.CheckState.Unchecked,
                    )
            # This gets called before constructor can finish, so add enabled font map here
            proc.disabled = not enabled
            self._mkFontMap()
            self.setFont(0, self.enabledFontMap[enabled])

    def updateFlags(self):
        # It's a shame super() doesn't return flags...
        super().updateFlags()
        opts = self.param.opts
        flags = self.flags()
        if opts["process"].allowDisable:
            flags |= QtCore.Qt.ItemFlag.ItemIsUserCheckable & (
                ~QtCore.Qt.ItemFlag.ItemIsAutoTristate
            )
        self.setFlags(flags)

    def setData(self, column, role, value):
        isChk = role == QtCore.Qt.ItemDataRole.CheckStateRole
        # Check for invalid request to change check state
        if isChk and self.param.parent() and not self.param.parent().opts["enabled"]:
            return
        checkstate = self.checkState(column)
        super().setData(column, role, value)
        if isChk and int(checkstate) != value:
            self.param.setOpts(enabled=bool(value))


class ProcGroupParameter(parameterTypes.GroupParameter):
    itemClass = ProcGroupParameterItem

    def setOpts(self, **opts):
        enabled = opts.get("enabled")
        curEnabled = self.opts["enabled"]
        super().setOpts(**opts)
        if enabled is not None and enabled != curEnabled:
            for chParam in filter(lambda el: isinstance(el, ProcGroupParameter), self):
                chParam.setOpts(enabled=enabled)


# WidgetParameterItem is not a QObject, so it can't emit signals. Use a dummy class instead
class _Emitter(QtCore.QObject):
    sigChanging = QtCore.Signal(object)
    sigChanged = QtCore.Signal(object)


class FilePickerParameterItem(parameterTypes.WidgetParameterItem):
    def makeWidget(self):
        param = self.param
        self._emitter = _Emitter()

        if param.opts["value"] is None:
            param.opts["value"] = ""
        fpath = param.opts["value"]
        param.opts.setdefault("asFolder", False)
        param.opts.setdefault("existing", True)
        button = QtWidgets.QPushButton()
        button.setValue = button.setText
        button.sigChanged = self._emitter.sigChanged
        button.value = button.text
        button.setText(fpath)
        button.clicked.connect(self._retrieveFolderNameGui)

        return button

    def _retrieveFolderNameGui(self):
        curVal = self.param.value()
        useDir = curVal or str(Path.cwd())
        opts = self.param.opts
        opts["startDir"] = str(Path(useDir).absolute())
        fname = popupFilePicker(None, "Select File", **opts)
        if fname is None:
            return
        self.param.setValue(fname)
        self._emitter.sigChanged.emit(fname)


class FilePickerParameter(Parameter):
    itemClass = FilePickerParameterItem


# Bugfix for pyqtgraph checklist in the meantime
class FixedChecklistParameter(ChecklistParameter):
    def __init__(self, **opts):
        opts.pop("children", None)
        super().__init__(**opts)

    def saveState(self, filter=None):
        state = super().saveState(filter)
        state.pop("children", None)
        return state


class NoneParameter(parameterTypes.SimpleParameter):
    def __init__(self, **opts):
        opts.update(readonly=True)
        super().__init__(**opts)

    def _interpretValue(self, v):
        return None


parameterTypes.registerParameterType("nonetype", NoneParameter, override=True)
parameterTypes.registerParameterType(
    "checklist", FixedChecklistParameter, override=True
)
parameterTypes.registerParameterType("NoneType", NoneParameter, override=True)
parameterTypes.registerParameterType("keyseq", KeySequenceParameter, override=True)
parameterTypes.registerParameterType("procgroup", ProcGroupParameter, override=True)
parameterTypes.registerParameterType(
    "shortcutkeyseq", ShortcutKeySeqParameter, override=True
)
parameterTypes.registerParameterType("shortcut", ShortcutParameter, override=True)
parameterTypes.registerParameterType(
    "popuplineeditor", PopupLineEditorParameter, override=True
)
parameterTypes.registerParameterType("filepicker", FilePickerParameter, override=True)
