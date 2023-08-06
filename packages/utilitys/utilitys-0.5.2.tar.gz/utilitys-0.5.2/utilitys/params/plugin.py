from __future__ import annotations

import weakref
from typing import Optional, Callable, Sequence

from pyqtgraph.Qt import QtWidgets, QtCore

from . import parameditor as pe, ShortcutParameter
from .prjparam import PrjParam
from ..fns import createAndAddMenuAct, paramWindow


class ParamEditorPlugin(pe.EditorPropsMixin):
    """
    Primitive plugin which can interface with window functionality. When this class is overloaded,
    the child class is given a reference to the main window and the main window is made aware of the
    plugin's existence. For interfacing with table fields, see the special case of
    :class:`TableFieldPlugin`
    """

    name: str = None
    """
  Name of this plugin as it should appear in the plugin menu
  """

    menu: QtWidgets.QMenu = None
    """
  Menu of additional options that should appear under this plugin
  """

    dock: Optional[pe.ParamEditorDockGrouping]
    """
  Docks that should be shown in a main window's menu bar. By default, just the toolsEditor is shown.
  If multiple param editors must be visible, manually set this property to a
  :class:`ParamEditorDockGrouping` as performed in :class:`TableFieldPlugin`.
  """
    toolsEditor: pe.ParamEditor
    """Param Editor window which holds user-editable properties exposed by the programmer"""

    _showFuncDetails = False
    """If *True*, a menu option will be added to edit parameters for functions that need them"""

    _makeMenuShortcuts = True
    """Whether shortcuts should be added to menu options"""

    _toolsEditorName: str = None
    """Name of the class tools editor. If not provided, defaults to '<class name> Tools'"""

    win = None
    """Reference to the application main window"""

    @property
    def parentMenu(self):
        """
        When this plugin is added, its options will be visible under a certain menu or toolbar. Where it is placed is
        determined by this value, which is usually the window's menu bar
        """
        return self.win.menuBar()

    def __initEditorParams__(self, **kwargs):
        """
        Creates most of the necessary components for interacting with editor properties including
        a dock that can be placed in a main window, a tools editor for registering properties and
        functions, and a dropdown menu for accessing these functions.
        """
        self.dock = pe.ParamEditorDockGrouping(dockName=self.name)
        self.toolsEditor = pe.ParamEditor.buildClsToolsEditor(
            type(self), self._toolsEditorName
        )
        if self._showFuncDetails:
            self.dock.addEditors([self.toolsEditor])
        menuName = self.name
        if "&" not in menuName:
            menuName = "&" + menuName
        self.menu = QtWidgets.QMenu(menuName)

    def __init__(self, *args, **kwargs):
        if self.dock is not None:
            self.dock.createMenuOpt(parentMenu=self.menu)
            self.menu.addSeparator()

    def registerFunc(
        self,
        func: Callable,
        submenuName: str = None,
        editor: pe.ParamEditor = None,
        **kwargs,
    ):
        """
        :param func: Function to register
        :param submenuName: If provided, this function is placed under a breakout menu with this name
        :param editor: If provided, the function is registered here instead of the plugin's tool editor
        :param kwargs: Forwarded to `ParamEditor.registerFunc`
        """
        if editor is None:
            editor = self.toolsEditor
        paramPath = []
        if submenuName is not None:
            paramPath.append(submenuName)
            parentMenu = None
            for act in self.menu.actions():
                if act.text() == submenuName and act.menu():
                    parentMenu = act.menu()
                    break
            if parentMenu is None:
                parentMenu = createAndAddMenuAct(editor, self.menu, submenuName, True)
                editor.params.addChild(dict(name=submenuName, type="group"))
        else:
            parentMenu = self.menu

        shcValue = opts = None
        owner = self
        if "btnOpts" in kwargs:
            opts = PrjParam(**kwargs["btnOpts"])
            owner = opts.opts.setdefault("ownerObj", self)
            kwargs.setdefault("name", opts.name)
            kwargs["btnOpts"] = opts
            shcValue = opts.value

        proc = editor.registerFunc(func, **kwargs)
        returnParam = kwargs.get("returnParam", False)
        if returnParam:
            proc, param = proc
        if parentMenu is not None:
            act = parentMenu.addAction(proc.name)
        if ShortcutParameter.REGISTRY and shcValue and self._makeMenuShortcuts:
            ShortcutParameter.REGISTRY.registerAction(
                opts, act, namePath=(owner.__groupingName__,)
            )

        act.triggered.connect(proc)

        # Win is provided by this plugin, so take it out of required keys if needed
        proc.input.keysFromPrevIO.discard("win")
        # Registration may have happened after attaching win ref, so ensure reference is valid here too
        proc.updateInput(win=self.win)
        if returnParam:
            return proc, param
        return proc

    def registerPopoutFuncs(
        self,
        funcList: Sequence[Callable],
        nameList: Sequence[str] = None,
        groupName: str = None,
        btnOpts: PrjParam = None,
    ):
        if groupName is None and btnOpts is None:
            raise ValueError("Must provide either group name or button options")
        elif btnOpts is None:
            btnOpts = PrjParam(groupName)
        if groupName is None:
            groupName = btnOpts.name
        act = self.menu.addAction(
            groupName, lambda: paramWindow(self.toolsEditor.params.child(groupName))
        )
        if nameList is None:
            nameList = [None] * len(funcList)
        for title, func in zip(nameList, funcList):
            self.toolsEditor.registerFunc(func, name=title, namePath=(groupName,))
        if ShortcutParameter.REGISTRY and btnOpts.value and self._makeMenuShortcuts:
            ShortcutParameter.REGISTRY.registerAction(
                btnOpts, act, namePath=(self.__groupingName__,)
            )

        self.menu.addSeparator()

    def attachWinRef(self, win):
        self.win = win
        if self.menu is not None and self.parentMenu is not None:
            self.menu.setParent(self.parentMenu, self.menu.windowFlags())
        for proc in self.toolsEditor.procToParamsMapping:
            proc.updateInput(win=win)
        if self.dock:
            self.dock.win = weakref.proxy(win)

    def addMenuToWindow(self, win: QtWidgets.QMainWindow, parentToolbarOrMenu=None):
        if parentToolbarOrMenu is None:
            parentToolbarOrMenu = win.menuBar()
        if isinstance(parentToolbarOrMenu, QtWidgets.QToolBar):
            btn = QtWidgets.QToolButton()
            btn.setText(self.name)
            parentToolbarOrMenu.addWidget(btn)
            parentToolbarOrMenu = btn
            btn.addMenu = btn.setMenu
            btn.addAction = lambda act: act.triggered.connect(btn.click)
            btn.setPopupMode(btn.InstantPopup)
        if self.menu is not None:
            parentToolbarOrMenu.addMenu(self.menu)

    @staticmethod
    def addDockToWindow(
        dock: QtWidgets.QDockWidget,
        win: QtWidgets.QMainWindow,
        dockArea: QtCore.Qt.DockWidgetArea = QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
    ):
        curAreaWidgets = [
            d
            for d in win.findChildren(QtWidgets.QDockWidget)
            if win.dockWidgetArea(d) == dockArea
        ]
        try:
            win.tabifyDockWidget(curAreaWidgets[-1], dock)
        except IndexError:
            # First dock in area
            win.addDockWidget(dockArea, dock)

    def addToWindow(
        self,
        win: QtWidgets.QMainWindow,
        parentToolbarOrMenu=None,
        dockArea: QtCore.Qt.DockWidgetArea = None,
    ):
        if parentToolbarOrMenu is not None:
            self.addMenuToWindow(win, parentToolbarOrMenu)
        if dockArea is not None:
            self.addDockToWindow(self.dock, win, dockArea)


def dockPluginFactory(name_: str = None, editors: Sequence[pe.ParamEditor] = None):
    class DummyPlugin(ParamEditorPlugin):
        name = name_

        def __initEditorParams__(self, **kwargs):
            super().__initEditorParams__(**kwargs)
            if editors is not None:
                self.dock.addEditors(editors)

    return DummyPlugin
