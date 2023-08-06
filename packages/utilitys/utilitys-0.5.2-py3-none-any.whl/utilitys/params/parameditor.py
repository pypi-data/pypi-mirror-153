import inspect
import typing as t
import warnings
import weakref
from contextlib import contextmanager
from pathlib import Path

from pyqtgraph.Qt import QtCore, QtWidgets, QtGui
from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from utilitys.widgets import EasyWidget
from . import PrjParam
from .procwrapper import addStageToParam
from .. import fns
from .._funcparse import RunOpts
from ..processing import *
from ..typeoverloads import FilePath

__all__ = [
    "RunOpts",
    "ParamEditor",
    "ParamEditorDockGrouping",
    "EditorPropsMixin",
    "SPAWNED_EDITORS",
    "ParamContainer",
]

Signal = QtCore.Signal


def _mkRunDict(proc: ProcessStage, btnOpts: t.Union[PrjParam, dict]):
    defaultBtnOpts = dict(name=proc.name, type="shortcut")
    if isinstance(btnOpts, PrjParam):
        # Replace falsy helptext with func signature
        btnOpts = btnOpts.toPgDict()
    if btnOpts is not None:
        # Make sure param type is not overridden
        btnOpts.pop("type", None)
        defaultBtnOpts.update(btnOpts)
    if len(defaultBtnOpts.get("tip", "")) == 0 and isinstance(proc, AtomicProcess):
        defaultBtnOpts["tip"] = fns.docParser(proc.fnDoc)["func-description"]
    if len(proc.input.hyperParamKeys) > 0:
        # In this case, a descriptive name isn't needed since the func name will be
        # present in the parameter group
        defaultBtnOpts["name"] = "Run"
    return defaultBtnOpts


"""
Eventually, it would be nice to implemenet a global search bar that can find/modify
any action, shortcut, etc. from any parameter. This tracker is an easy way to fascilitate
such a feature. A `class:FRPopupLineEditor` can be created with a model derived from
all parameters from SPAWNED_EDITORS, thereby letting a user see any option from any
param editor.
"""


class ParamEditor(QtWidgets.QDockWidget):
    sigParamStateCreated = Signal(str)
    sigChangesApplied = Signal(object)
    # Dict of changes, or *None*
    sigParamStateDeleted = Signal(str)

    _baseRegisterPath: t.Sequence[str] = ()
    """
  Classes typically register all their properites in bulk under the same group of
  parameters. This property will be overridden (see :meth:`setBaseRegisterPath`) by
  the class name of whatever class is currently registering properties.
  """

    def __init__(
        self,
        parent=None,
        paramList: t.List[t.Dict] = None,
        saveDir: FilePath = None,
        fileType="param",
        name=None,
        treeChildren: t.Union[Parameter, t.List[Parameter]] = None,
        **kwargs,
    ):
        """
        GUI controls for user-interactive parameters within a QtWidget (usually main window). Each window consists of
        a parameter tree and basic saving capabilities.

        :param parent: GUI parent of this window
        :param paramList: User-editable parameters. This is often *None* and parameters
          are added dynamically within the code.
        :param saveDir: When "save" is performed, the resulting settings will be saved
          here.
        :param fileType: The filetype of the saved settings. E.g. if a settings configuration
          is saved with the name "test", it will result in a file "test.&lt;fileType&gt;"
        :param name: User-readable name of this parameter editor
        :param topTreeChild: List of tree parameters. Since the default pyqtgraph TreeWidget doesn't easily allow inserting
          a new parameter *before* an existing one, this allows specifying a different ordering of top-level tree children.
          Since self.params will need to be specified in almost all cases, use *None* to specify where in the list it
          should occur. In most cases, this can be left as *None* in which case self.params will be the top and only tree
          child on startup.
        """
        super().__init__(parent)
        self.hide()
        cls = type(self)
        # Place in list so an empty value gets unpacked into super constructor
        if paramList is None:
            paramList = []
        if name is None:
            name = fns.nameFormatter(fns.clsNameOrGroup(cls).replace("Editor", ""))

        if saveDir is not None:
            saveDir = Path(saveDir)

        self.registeredPrjParams: t.List[PrjParam] = []
        """
    Keeps track of all parameters registerd as properties in this editor. Useful for
    inspecting which parameters are in an editor without traversing the parameter tree
    and reconstructing the name, tooltip, etc.
    """

        self.procToParamsMapping: t.Dict[ProcessStage, GroupParameter] = {}
        """
    Keeps track of registered functions (or prcesses) and their associated
    gui parameters
    """

        self.dock = self
        """Records whether this is a standalone dock or nested inside a ParamEditorDockGrouping"""

        self.name = name
        """Human readable name (for settings menu)"""

        self.saveDir = saveDir
        """Internal parameters for saving settings"""
        self.fileType = fileType
        """Used under the hood to name saved states"""

        self.savedStates: t.List[str] = []
        """Records which states are available since the last change"""

        self.watcher = QtCore.QFileSystemWatcher()
        """Responsible for detecting changes in the saved states"""
        if self.saveDir is not None:
            self.saveDir.mkdir(parents=True, exist_ok=True)
            self.watcher.addPath(str(self.saveDir))
        self.watcher.directoryChanged.connect(lambda: self.updateSavedStates())
        self.watcher.fileChanged.connect(self._maybeUpdateCurState)

        # -----------
        # Construct parameter tree
        # -----------
        self.params = Parameter.create(
            name="Parameters", type="group", children=paramList
        )

        if treeChildren is None:
            treeChildren = self.params
        if isinstance(treeChildren, Parameter):
            treeChildren = [treeChildren]
        for ii, ch in enumerate(treeChildren):
            if not ch:
                treeChildren[ii] = self.params
        self.tree = fns.flexibleParamTree(treeChildren, showTop=False)

        self.stateName = None
        self._lastAppliedState: t.Optional[dict] = None

        self._buildGui()

        # Redefine here to avoid excess parameters and make nice name
        def niceStateLoader(loadState="Default"):
            """
            :param loadState:
              pType: popuplineeditor
              limits: ['Default']
            """
            if loadState in self.savedStates and loadState != self.stateName:
                return self.loadParamValues(loadState)

        proc, param = self.registerFunc(
            niceStateLoader,
            namePath=(),
            overrideBasePath=(),
            nest=False,
            returnParam=True,
            parentParam=self._metaParamGrp,
            runOpts=RunOpts.ON_CHANGED,
        )
        # Hide this from the global registry to avoid menu option creation
        del self.procToParamsMapping[proc]
        self.stateSelector = param.child("loadState")

        # Populate initial values, avoid early trigger of load values
        if self.saveDir:
            self.updateSavedStates()
        else:
            self._metaTree.hide()
            param.hide()

        SPAWNED_EDITORS.append(weakref.proxy(self))

    def _maybeUpdateCurState(self, file: str):
        """Defined as an outer function since it has to be disabled sometimes (e.g. during save to same name)"""
        if Path(file) == self.formatFileName(self.stateName):
            # Time for a reload, Put in event loop to allow file time to save
            # TODO: 5 ms might not be long enough for a file save, figure out a good
            #   way of waiting the right amount of time
            QtCore.QTimer.singleShot(5, lambda: self.loadParamValues(self.stateName))

    def applyChanges(self, newName: FilePath = None, newState: dict = None):
        """
        Broadcasts that this parameter editor has updated changes

        :param newName: Name of the applied state. If *None*, stateName is used
        :param newState: Dict representation of the new state. If *None*, the most recently
          applied state is used
        """
        if newName is None:
            newName = self.stateName
        if newState is None:
            newState = self._lastAppliedState

        if newName:
            newName = Path(newName).stem

        self.sigChangesApplied.emit(newState)

        if self.stateName == newName:
            return
        self.watcher.removePath(str(self.formatFileName()))
        self.stateName = newName
        self.watcher.addPath(str(self.formatFileName()))
        self.stateSelector.setValue(self.stateName)
        return newState

    def saveParamValues(
        self,
        saveName: str = None,
        paramState: dict = None,
        *,
        allowOverwriteDefault=False,
        includeDefaults=False,
        blockWrite=False,
        applyChanges=True,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """
        * Returns dict on successful parameter save and emits sigParamStateCreated.
        * Returns None if no save name was given
        """
        if (saveName is None or self.saveDir is None) and not blockWrite:
            return None
        elif paramState is None:
            paramState = fns.paramValues(
                self.params, includeDefaults=includeDefaults or allowOverwriteDefault
            )
            # Unnest 'parameters' name
            paramState = paramState.get("Parameters", {})
            # Nothing changed for this state, no need to do any updating
            applyChanges = False
        # Remove non-useful values
        if not blockWrite and self.saveDir is not None:
            # This shouldn't cause a self-reload
            self.watcher.fileChanged.disconnect(self._maybeUpdateCurState)
            try:
                fns.saveToFile(
                    paramState,
                    self.formatFileName(saveName),
                    allowOverwriteDefault=allowOverwriteDefault,
                )
            finally:
                self.watcher.fileChanged.connect(self._maybeUpdateCurState)
        if applyChanges:
            # Since save state shouldn't be modifying the current state, it will emit the same
            # state as before, but under a new name -- regardless of the param state dict
            self.applyChanges(saveName)
        return paramState

    def saveCurStateAsDefault(self):
        self.saveParamValues("Default", allowOverwriteDefault=True)
        self.stateName = "Default"

    def _loadParamState(
        self, stateName: str, stateDict: dict = None, applyChanges=True
    ):
        # Bug in pyqtgraph restore state doesn't play nice when parameters have connected functions outside the parameter
        # item, so re-implement without inserting or removing children
        loadDict = self._parseStateDict(stateName, stateDict)
        with self.params.treeChangeBlocker():
            fns.applyParamOpts(self.params, loadDict)
        if applyChanges:
            self.applyChanges(stateName, stateDict)
        return loadDict

    def _parseAndUpdateCandidateParams(
        self, loadDict: dict, candidateParams: t.Sequence[Parameter]
    ):
        def validName(param, name):
            return name in (param.opts["title"], param.name())

        def checkParentChain(param, name):
            if not param:
                return False
            return validName(param, name) or checkParentChain(param.parent(), name)

        unhandled = {}
        # Copy for mutable object
        for kk, vv in loadDict.items():
            if isinstance(vv, dict):
                # Successively traverse down child tree
                curCandidates = [p for p in candidateParams if checkParentChain(p, kk)]
                # By this point defaults are already populated so no need to reset them otherwise infinite recursion will occur
                self.loadParamValues(
                    "",
                    vv,
                    useDefaults=False,
                    candidateParams=curCandidates,
                    applyChanges=False,
                )
            else:
                unhandled[kk] = vv
        with self.params.treeChangeBlocker():
            for kk, vv in unhandled.items():
                matches = [p for p in candidateParams if validName(p, kk)]
                if len(matches) == 1:
                    matches[0].setValue(vv)
                # elif len(matches) == 0:
                #   warnings.warn(f'No matching parameters for key {kk}. Ignoring.', UserWarning)
                elif len(matches) > 0:
                    raise ValueError(
                        f"Multiple matching parameters for key {kk}:\n" f"{matches}"
                    )

    def loadParamValues(
        self,
        stateName: t.Union[str, Path],
        stateDict: dict = None,
        useDefaults=True,
        candidateParams: t.List[Parameter] = None,
        applyChanges=True,
    ):
        """
        Can restore a state created by `fns.paramValues`

        :param stateName: State name to load, see ParamEditor.saveParamValues
        :param stateDict: Override the state name values by providing a dict instead to prevent file IO
        :param useDefaults: Whether default values should be used for all unspecified state values. If not, only the
          specified keys will be updated.
        :param candidateParams: set of parameters these settings should apply to. If *None*, defaults to all parameters in
          this editor
        :param applyChanges: Whether to trigger `sigChangesApplied` after load.
        :return: Loaded state
        """
        loadDict = self._parseStateDict(stateName, stateDict)
        # First check for extra keys, will be the case if 'children' is one of the keys. Can't do value-loading in that case,
        # must do state-loading instead
        if "children" in loadDict:
            return self._loadParamState(stateName, stateDict)

        defaultFile = self.formatFileName("Default")
        if useDefaults and defaultFile and defaultFile.exists():
            base = fns.attemptFileLoad(defaultFile) or {}
            loadDict = fns.hierarchicalUpdate(base, loadDict, replaceLists=True)

        if candidateParams is None:
            candidateParams = fns.paramsFlattened(self.params)

        if candidateParams:
            self._parseAndUpdateCandidateParams(loadDict, candidateParams)

        if applyChanges:
            self.applyChanges(stateName, loadDict)
        return fns.paramValues(self.params, includeDefaults=True)

    def formatFileName(self, stateName: t.Union[str, Path] = None):
        if stateName is None:
            stateName = self.stateName
        suffix = f".{self.fileType}"
        stateName = stateName or suffix
        stateName = Path(stateName)
        if self.saveDir is None:
            # Prevents ValueError at the final return
            return stateName
        elif not stateName.is_absolute():
            stateName = self.saveDir / stateName
        if not stateName.suffix:
            stateName = stateName.with_suffix(suffix)
        return stateName

    def _parseStateDict(self, stateName: t.Union[str, Path], stateDict: dict = None):
        _, stateDict = fns.resolveYamlDict(self.formatFileName(stateName), stateDict)
        if "Parameters" in stateDict:
            warnings.warn(
                '"Parameters" is deprecated for a loaded state. In the future, set options at the'
                " top dictionary level",
                DeprecationWarning,
                stacklevel=2,
            )
            subDict = stateDict.pop("Parameters")
            if subDict:
                stateDict.update(subDict)
        return stateDict

    def deleteParamState(self, stateName: str):
        filename = self.formatFileName(stateName)
        if not filename.exists():
            return
        filename.unlink()

    def registerProps(self, constParams: t.List[PrjParam], *args, **kwargs):
        """
        Registers a list of proerties and returns an array of each. For parameter descriptions,
        see :func:`PrjParamEditor.registerProp`.
        """
        outProps = []
        with self.params.treeChangeBlocker():
            for param in constParams:
                outProps.append(self.registerProp(param, *args, **kwargs))
        return outProps

    def _resolveNamePath(self, namePath):
        if namePath is None:
            namePath = self._baseRegisterPath
        elif isinstance(namePath, str):
            namePath = (namePath,)
        return namePath

    def registerProp(
        self,
        constParam: PrjParam = None,
        namePath: t.Union[t.Sequence[str], str] = None,
        container: ParamContainer = None,
        **etxraOpts,
    ):
        """
        Registers a property defined by *constParam* that will appear in the respective
        parameter editor.

        :param constParam: Object holding parameter attributes such as name, type,
          help text, etc. If *None*, defaults to a 'group' type
        :param namePath: If None, defaults to the top level of the parameters for the
          current class (or paramHolder). *namePath* represents the parent group
          to whom the newly registered parameter should be added
        :param container: Optional container in which to insert this parameter
        :param etxraOpts: Extra options passed directly to the created :class:`pyqtgraph.Parameter`

        :return: Property bound to this value in the parameter editor
        """
        paramOpts = constParam.toPgDict()
        paramOpts.update(etxraOpts)

        namePath = self._resolveNamePath(namePath)
        paramForEditor = fns.getParamChild(self.params, *namePath, chOpts=paramOpts)

        self.registeredPrjParams.append(constParam)
        if container is not None:
            container[constParam] = paramForEditor
        return paramForEditor

    def registerFunc(
        self,
        func: t.Callable,
        *,
        runOpts=RunOpts.ON_BUTTON,
        namePath: t.Union[t.Sequence[str], str] = None,
        paramFormat=None,
        btnOpts: t.Union[PrjParam, dict] = None,
        nest=True,
        parentParam: Parameter = None,
        returnParam=False,
        container: ParamContainer = None,
        **kwargs,
    ):
        """
        Like `registerProp`, but for functions instead along with interactive parameters
        for each argument. A button is added for the user to force run this function as
        well. In the case of a function with no parameters, the button will be named
        the same as the function itself for simplicity

        :param namePath:  See `registerProp`
        :param func: Function to make interactive
        :param runOpts: Combination of ways this function can be run. Multiple of these
          options can be selected at the same time using the `|` operator.
            * If RunOpts.ON_BUTTON, a button is present as described.
            * If RunOpts.ON_CHANGE, the function is run when parameter values are
              finished being changed by the user
            * If RunOpts.ON_CHANGING, the function is run every time a value is altered,
              even if the value isn't finished changing.
        :param paramFormat: Formatter which turns variable names into display names. The default takes variables in pascal
          case (e.g. variableName) or snake case (e.g. variable_name) and converts to Title Case (e.g. Variable Name).
          Custom functions must have the signature (str) -> str. To change default behavior, see `nameFormat.set()`.
        :param btnOpts: Overrides defaults for button used to run this function. If
          `RunOpts.ON_BUTTON` is not in `RunOpts`, these values are ignored.
        :param nest: If *True*, functions with multiple default arguments will have these nested
          inside a group parameter bearing the function name. Otherwise, they will be added
          directly to the parent parameter specified by `namePath` + `baseRegisterPath`
        :param returnParam: Whether to return the parent parameter associated with this newly
          registered function
        :param parentParam: Which parent should hold this registered function. If None, defaults to `self.param
        :param container: Container in which to put child parameters from the registered function. This has a similar effect
          to calling `registerProps` on each of the function arguments with this container. *Note*: while the former will
          register props according to the `constParam` PrjParam, this will register to the container using the raw parameter
          name. A KeyError is raised when a new parameter name clashes with something already in the container.
        :param kwargs: All additional kwargs are passed to AtomicProcess when wrapping the function.
        """
        if not isinstance(func, ProcessStage):
            proc: ProcessStage = AtomicProcess(func, **kwargs)
            proc.cacheOnEq = False
        else:
            proc = func
        # Define caller out here that takes no params so qt signal binding doesn't
        # screw up auto parameter population
        def runProc():
            return proc.run()

        def runpProcOnChanging(_param: Parameter, newVal: t.Any):
            forwardedOpts = ProcessIO(**{_param.name(): newVal})
            return proc.run(forwardedOpts)

        namePath = self._resolveNamePath(namePath)
        if parentParam is None:
            parentParam = self.params
        topParam = fns.getParamChild(parentParam, *namePath)
        if len(proc.input.hyperParamKeys) > 0:
            # Check if proc params already exist from a previous addition
            parentParam = addStageToParam(
                proc, topParam, argNameFormat=paramFormat, nestHyperparams=nest
            )
            for param in proc.input.params.values():
                if RunOpts.ON_CHANGED in runOpts:
                    param.sigValueChanged.connect(runProc)
                if RunOpts.ON_CHANGING in runOpts:
                    param.sigValueChanging.connect(runpProcOnChanging)
        else:
            parentParam: GroupParameter = topParam
        if RunOpts.ON_BUTTON in runOpts:
            runBtnDict = _mkRunDict(proc, btnOpts)
            if not nest:
                # Make sure button name is correct
                runBtnDict["name"] = proc.name
            runBtn = fns.getParamChild(parentParam, chOpts=runBtnDict)
            runBtn.sigActivated.connect(runProc)
        self.procToParamsMapping[proc] = parentParam

        if container is not None:
            for pName in proc.input.hyperParamKeys:
                if pName in container.keys():
                    raise KeyError(f"{pName} already exists in this container")
                container[pName] = parentParam.child(pName)

        if returnParam:
            return proc, parentParam
        return proc

    @classmethod
    def buildClsToolsEditor(cls, forCls: type, name: str = None):
        groupName = fns.clsNameOrGroup(forCls)
        lowerGroupName = groupName.lower()
        if name is None:
            name = groupName
        if not name.endswith("Tools"):
            name = name + " Tools"
        toolsEditor = cls(fileType=lowerGroupName.replace(" ", ""), name=name)
        for widget in (toolsEditor.saveAsBtn, toolsEditor.applyBtn):
            widget.hide()
        return toolsEditor

    def createMenuOpt(self, overrideName=None, parentMenu: QtWidgets.QMenu = None):
        if overrideName is None:
            overrideName = self.name
        editAct = QtGui.QAction("Open " + overrideName, self)
        if self.saveDir is None:
            # No save options are possible, just use an action instead of dropdown menu
            newMenuOrAct = editAct
            if parentMenu is not None:
                parentMenu.addAction(newMenuOrAct)
        else:
            newMenuOrAct = QtWidgets.QMenu(overrideName, self)
            newMenuOrAct.addAction(editAct)
            newMenuOrAct.addSeparator()

            def populateFunc():
                self.addDirItemsToMenu(newMenuOrAct)

            self.sigParamStateCreated.connect(populateFunc)
            self.sigParamStateDeleted.connect(populateFunc)
            # Initialize default menus
            populateFunc()
            if parentMenu is not None:
                parentMenu.addMenu(newMenuOrAct)
        editAct.triggered.connect(self.show)
        return newMenuOrAct

    def actionsMenuFromProcs(
        self,
        title: str = None,
        nest=True,
        parent: QtWidgets.QWidget = None,
        outerMenu: QtWidgets.QMenu = None,
    ):
        title = title or self.dock.name
        if nest and outerMenu:
            menu = QtWidgets.QMenu(title, parent)
            outerMenu.addMenu(menu)
        elif outerMenu:
            menu = outerMenu
        else:
            menu = QtWidgets.QMenu(title, parent)
        for proc in self.procToParamsMapping:
            menu.addAction(proc.name, lambda _p=proc: _p.run())
        return menu

    def updateSavedStates(self, blockLoad=True):
        """
        Evaluates this directory's saved states and exposes them to the application

        :param blockLoad: It is posisble for the current state to be deleted, in which case this call will force load the
          next possible state. When `blockLoad` is *True*, this will not happen.
        """
        dirGlob = list(self.saveDir.glob(f"*.{self.fileType}"))
        dirStates = [f.stem for f in dirGlob]

        newStates = set(dirStates) - set(self.savedStates)
        delStates = set(self.savedStates) - set(dirStates)

        self.savedStates = dirStates
        # Kind of a hack: Make sure no sigValueChange is emmittedto until after setLimits
        oldSig = self.stateSelector.sigValueChanged
        if blockLoad:
            self.stateSelector.sigValueChanged = fns.DummySignal()
        try:
            self.stateSelector.setLimits(self.savedStates)
        finally:
            self.stateSelector.sigValueChanged = oldSig
        for state in newStates:
            self.sigParamStateCreated.emit(state)
        for state in delStates:
            self.sigParamStateDeleted.emit(state)

    def addDirItemsToMenu(
        self, parentMenu: QtWidgets.QMenu, removeExistingChildren=True
    ):
        """Helper function for populating menu from directory contents"""
        # We don't want all menu children to be removed, since this would also remove the 'edit' and
        # separator options. So, do this step manually. Remove all actions after the separator
        if self.saveDir is None:
            return
        dirGlob = self.saveDir.glob(f"*.{self.fileType}")
        # Define outside for range due to loop scoping
        def _loader(name):
            def _call():
                self.loadParamValues(name)

            return _call

        if removeExistingChildren:
            encounteredSep = False
            for ii, action in enumerate(parentMenu.children()):
                action: QtGui.QAction
                if encounteredSep:
                    parentMenu.removeAction(action)
                elif action.isSeparator():
                    encounteredSep = True
        # TODO: At the moment param files that start with '.' aren't getting included in the
        #  glob
        for name in dirGlob:
            # glob returns entire filepath, so keep only filename as layout name
            name = name.with_suffix("").name
            curAction = parentMenu.addAction(name)
            curAction.triggered.connect(_loader(name))

    @classmethod
    @contextmanager
    def setBaseRegisterPath(cls, *path: str):
        oldPath = cls._baseRegisterPath
        cls._baseRegisterPath = path
        yield
        cls._baseRegisterPath = oldPath

    def _buildGui(self, **kwargs):
        self.setWindowTitle(self.name)
        self.setObjectName(self.name)

        # -----------
        # Additional widget buttons
        # -----------
        self.expandAllBtn = QtWidgets.QPushButton("Expand All")
        self.collapseAllBtn = QtWidgets.QPushButton("Collapse All")
        self.saveAsBtn = QtWidgets.QPushButton("Save As...")
        self.applyBtn = QtWidgets.QPushButton("Apply")

        # -----------
        # Widget layout
        # -----------
        self._mkMetaTree()

        self.treeBtnsWidget = EasyWidget([self.expandAllBtn, self.collapseAllBtn])
        children = [
            self.treeBtnsWidget,
            EasyWidget([self._metaTree, self.tree], layout="V", useSplitter=True),
            [self.saveAsBtn, self.applyBtn],
        ]

        self.dockContentsWidget = EasyWidget.buildWidget(children)

        if self.saveDir is None:
            self.saveAsBtn.hide()
            self.treeBtnsWidget.widget_.hide()

        self.centralLayout = self.dockContentsWidget.easyChild.layout_
        self.setWidget(self.dockContentsWidget)

        # self.setLayout(centralLayout)
        self.tree.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        # -----------
        # UI Element Signals
        # -----------
        self.expandAllBtn.clicked.connect(lambda: fns.setParamsExpanded(self.tree))
        self.collapseAllBtn.clicked.connect(
            lambda: fns.setParamsExpanded(self.tree, False)
        )
        self.saveAsBtn.clicked.connect(self.saveParamValuesGui)
        self.applyBtn.clicked.connect(lambda: self.applyChanges())

    def _mkMetaTree(self):
        self._metaParamGrp = Parameter.create(name="Meta Parameters", type="group")
        mt = self._metaTree = fns.flexibleParamTree(self._metaParamGrp, showTop=False)
        """
    Tree for controlling meta-parameters, useful for configuring the parameter editor itself
    (i.e. loading state, etc.)
    """
        self._metaParamGrp.sigChildAdded.connect(
            lambda: mt.setMinimumHeight(int(mt.sizeHint().height() * 1.1))
        )
        return self._metaTree, self._metaParamGrp

    def __repr__(self):
        selfCls = type(self)
        oldName: str = super().__repr__()
        # Remove module name for brevity
        oldName = oldName.replace(
            f"{selfCls.__module__}.{selfCls.__name__}",
            f"{selfCls.__name__} '{self.name}'",
        )
        return oldName

    def show(self):
        if self.dock is self:
            return super().show()
        if isinstance(self.dock, ParamEditorDockGrouping):
            tabs: QtWidgets.QTabWidget = self.dock.tabs
            dockIdx = tabs.indexOf(self.dockContentsWidget)
            tabs.setCurrentIndex(dockIdx)
        # Necessary on MacOS
        self.dock.setWindowState(QtCore.Qt.WindowState.WindowActive)
        self.dock.raise_()
        self.dock.show()
        # Necessary on Windows
        self.activateWindow()
        self.applyBtn.setFocus()

    def reject(self):
        """
        If window is closed apart from pressing 'accept', restore pre-edit state
        """
        self.params.restoreState(self._stateBeforeEdit, removeChildren=False)
        super().reject()

    def saveParamValuesGui(self):
        saveName = fns.dialogGetSaveFileName(self, "Save As", self.stateName)
        self.saveParamValues(saveName)


class ParamEditorDockGrouping(QtWidgets.QDockWidget):
    """
    When multiple parameter editor windows should be grouped under the same heading,
    this class is responsible for performing that grouping.
    """

    def __init__(
        self, editors: t.List[ParamEditor] = None, dockName: str = "", parent=None
    ):
        super().__init__(parent)
        self.tabs = QtWidgets.QTabWidget(self)
        self.hide()

        if dockName is None:
            dockName = ""

        if editors is None:
            editors = []
        if len(dockName) == 0 and len(editors) > 0:
            dockName = editors[0].name
        dockName = dockName.replace("&", "")
        self.name = dockName

        self.editors = []
        self.addEditors(editors)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setWidget(centralWidget)
        self.setObjectName(dockName)
        self.setWindowTitle(dockName)

        self.biggestMinWidth = 0

        self.win = None
        """Reference to main window if added to one, to resize docks to required width"""

    def addEditors(self, editors: t.Sequence[ParamEditor]):
        minWidth = 0
        for editor in editors:
            if editor.width() > minWidth:
                minWidth = int(editor.width() * 0.8)
            # "Main Image Settings" -> "Settings"
            tabName = self.getTabName(editor)
            self.tabs.addTab(editor.dockContentsWidget, tabName)
            editor.dock = self
            self.editors.append(editor)
        self.biggestMinWidth = minWidth

    def removeEditors(self, editors: t.Sequence[ParamEditor]):
        for editor in editors:
            idx = self.editors.index(editor)
            self.tabs.removeTab(idx)
            editor.dock = editor
            del self.editors[idx]

    def setParent(self, parent: QtWidgets.QWidget = None):
        super().setParent(parent)
        for editor in self.editors:
            editor.setParent(parent)

    def getTabName(self, editor: ParamEditor):
        if self.name in editor.name and len(self.name) > 0:
            tabName = editor.name.split(self.name)[1][1:]
            if len(tabName) == 0:
                tabName = editor.name
        else:
            tabName = editor.name
        return tabName

    def createMenuOpt(self, overrideName=None, parentMenu: QtWidgets.QMenu = None):
        if overrideName is None:
            overrideName = self.name
        if parentMenu is None:
            parentMenu = QtWidgets.QMenu(overrideName, self)
        # newMenu = create_addMenuAct(self, parentBtn, dockEditor.name, True)
        for editor in self.editors:  # type: ParamEditor
            # "Main Image Settings" -> "Settings"
            tabName = self.getTabName(editor)
            nameWithoutBase = tabName
            editor.createMenuOpt(overrideName=nameWithoutBase, parentMenu=parentMenu)
        return parentMenu

    def showEvent(self, ev: QtGui.QShowEvent):
        super().showEvent(ev)
        self.raise_()
        self.activateWindow()
        if self.width() < self.biggestMinWidth + 100 and self.win:
            self.win.resizeDocks(
                [self], [self.biggestMinWidth + 100], QtCore.Qt.Orientation.Horizontal
            )


# Use QObject base type to allow inheritence within the Qt framework
class EditorPropsMeta(type(QtCore.QObject)):
    __editorPropertyOpts = {}
    """Options passed to kwargs during __initEditorParams__"""

    def __call__(cls, *args, **kwargs):
        cls.resolveGroupingName()
        basePath = (cls.__groupingName__,)
        if basePath[0] == "":
            basePath = ()

        obj = cls.__new__(cls, *args, **kwargs)

        with ParamEditor.setBaseRegisterPath(*basePath):
            obj.__initEditorParams__(**cls._getBoundPropertyOpts(obj))
            obj.__init__(*args, **kwargs)
        return obj

    def resolveGroupingName(cls):
        # ParamEditor case
        if (
            hasattr(cls, "name")
            and cls.name is not None
            and cls.__groupingName__ is None
        ):
            # The '&' character can be used in Qt to signal a shortcut, which is used internally
            # by plugins. When these plugins register shortcuts, the group name will contain
            # ampersands which shouldn't show up in human readable menus
            cls.__groupingName__ = cls.name.replace("&", "")
        if cls.__groupingName__ is None:
            cls.__groupingName__ = fns.nameFormatter(cls.__name__)

    def _getBoundPropertyOpts(cls, obj):
        sig = inspect.signature(obj.__initEditorParams__)
        ret = {}
        for kk, vv in sig.parameters.items():
            if vv.kind is vv.VAR_KEYWORD:
                # if keywords are allowed, all properties can be passed
                return cls.__editorPropertyOpts
            elif kk in cls.__editorPropertyOpts:
                ret[kk] = cls.__editorPropertyOpts[kk]
        return ret

        ret = {
            k: cls.__editorPropertyOpts[k]
            for k in set(sig.parameters).intersection(cls.__editorPropertyOpts)
        }

    @contextmanager
    def setEditorPropertyOpts(cls, **opts):
        """
        sets the optios accociated with calls to __initEditorParams__ for instances of this class
        created inside the context manager
        """
        oldOpts = cls.__editorPropertyOpts.copy()
        cls.__editorPropertyOpts.update(opts)
        yield
        cls.__editorPropertyOpts.update(oldOpts)
        for newKey in set(cls.__editorPropertyOpts).difference(oldOpts):
            del cls.__editorPropertyOpts[newKey]


class EditorPropsMixin(metaclass=EditorPropsMeta):
    __groupingName__: str = None

    def __initEditorParams__(self, **kwargs):
        pass


SPAWNED_EDITORS: t.List[ParamEditor] = []
