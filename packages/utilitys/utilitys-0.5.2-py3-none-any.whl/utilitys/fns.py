import ast
import html
import inspect
import multiprocessing as mp
import re
import sys
import argparse
import typing as t
import warnings
from argparse import Namespace
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from traceback import format_exception
from warnings import warn
import signal
import logging

import docstring_parser as dp
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui, QT_LIB
from pyqtgraph.parametertree import Parameter, ParameterTree
from tqdm import tqdm

from .params import PrjParam
from .typeoverloads import FilePath
from .constants import PrjEnums

# -----
# For Pyyaml
# -----
# import yaml
# from yaml import YAMLError
# loader = yaml.UnsafeLoader
# dumper = yaml.Dumper
# def yamlLoad(stream):
#   return yaml.load(stream, loader)
# def yamlDump(data, stream):
#   return yaml.dump(data, stream, dumper, sort_keys=False)

# -----
# For ruamel yaml
# -----
from ruamel.yaml import YAML, YAMLError

dumper = YAML()
loader = YAML(typ="safe")


def yamlLoad(stream):
    return loader.load(stream)


def yamlDump(data, stream):
    return dumper.dump(data, stream)


def docParser(docstring: str, streamFormat="ini"):
    from ._funcparse import docParser as _dp

    return _dp(docstring, streamFormat)


def funcToParamDict(func, title=None, **overrides):
    from ._funcparse import funcToParamDict as _fpd

    return _fpd(func, title, **overrides)


def mprocApply(
    func,
    iterLst,
    descr="",
    iterArgPos=0,
    extraArgs=(),
    showProgress=True,
    applyAsync=True,
    total=None,
    pool=None,
    processes=None,
    debug=False,
    discardReturnValues=False,
    **extraKwargs,
):
    if total is None:
        try:
            total = len(iterLst)
        except (AttributeError, TypeError):
            total = None

    callback = None
    if showProgress and applyAsync and not debug:
        progBar = tqdm(total=total, desc=descr)

        def updateProgBar(*_):
            progBar.update()

        callback = updateProgBar
    elif showProgress:
        iterLst = tqdm(iterLst, total=total, desc=descr)

    pre_results = []
    errs = {}

    def errCallback(fnArgs, ex):
        errs[str(fnArgs[iterArgPos])] = str(ex)

    if debug:

        def applyFunc(func_, args):
            return func_(*args, **extraKwargs)

    else:
        if pool is None:
            pool = mp.Pool(processes)
        if applyAsync:

            def applyFunc(func_, args):
                return pool.apply_async(
                    func_,
                    args,
                    kwds=extraKwargs,
                    callback=callback,
                    error_callback=lambda ex: errCallback(args, ex),
                )

        else:
            applyFunc = pool.apply

    extraArgs = tuple(extraArgs)
    for el in iterLst:
        curArgs = extraArgs[:iterArgPos] + (el,) + extraArgs[iterArgPos:]
        pre_results.append(applyFunc(func, curArgs))
    if not debug:
        pool.close()
        pool.join()
    if len(errs) > 0:
        msg = f"The following errors occurred at the specified list indices:\n"
        for k, v in errs.items():
            msg += f"{k}: {v}\n"
        warn(msg)
    if discardReturnValues:
        return
    if applyAsync and not debug:
        return [res.get() for res in pre_results]
    else:
        return pre_results


def mproc_apply(*args, **kwargs):
    warn("'mproc_apply' is deprecated, please use 'mprocApply'", DeprecationWarning)
    return mprocApply(*args, **kwargs)


def dynamicDocstring(embed=False, **kwargs):
    """
    Docstrings must be known at compile time. However this prevents expressions like

    ```
    x = ['dog', 'cat', 'squirrel']
    def a(animal: str):
      \"\"\"
      param animal: must be one of {x}
      \"\"\"
    ```

    from compiling. This can make some featurs of function registration difficult, like dynamically generating
    limits for a docstring list. `dynamicDocstring` wrapps a docstring and provides kwargs
    for string formatting.
    Retrieved from https://stackoverflow.com/a/10308363/9463643

    :param embed: Sometimes, the value that should be accessed from the docstring is not recoverable from its string
      representation. YAML knows how to serialize the default types, but it is a pain to write a deserialization protocol
      for every object used as a dynamic reference. To avoid this, `embed` determines whether a `__docObjs__` reference
      should eb attached to the function with the raw object values. I.e. instead of storing the string representation of
      a list kwarg, __docObjs__ would hold a reference to the list itself.
    :param kwargs: List of kwargs to pass to formatted docstring
    """

    def wrapper(obj):
        obj.__doc__ = obj.__doc__.format(**kwargs)
        if embed:
            obj.__docObjs__ = kwargs
        return obj

    return wrapper


def serAsFrame(ser: pd.Series):
    return ser.to_frame().T


def createAndAddMenuAct(
    mainWin: QtWidgets.QWidget, parentMenu: QtWidgets.QMenu, title: str, asMenu=False
) -> t.Union[QtWidgets.QMenu, QtGui.QAction]:
    menu = None
    if asMenu:
        menu = QtWidgets.QMenu(title, mainWin)
        act = menu.menuAction()
    else:
        act = QtGui.QAction(title)
    parentMenu.addAction(act)
    if asMenu:
        return menu
    else:
        return act


old_showwarning = warnings.showwarning
old_sys_except_hook = sys.excepthook
usingPostponedErrors = False
_eType = t.Union[t.Type[Exception], t.Type[Warning]]


class AppLogger(logging.Logger):
    nonCriticalErrors = ()

    old_showwarning = None
    old_sys_excepthook = None

    def logLater(self, msg, *args, **kwargs):
        # Define local function to avoid uncollected garbage on pyside2
        def doLog():
            self.log(msg, *args, **kwargs)

        QtCore.QTimer.singleShot(0, doLog)

    def attention(self, msg, *args, **kwargs):
        return self.log(PrjEnums.LOG_LVL_ATTN, msg, *args, **kwargs)

    def registerExceptions(
        self, win: QtWidgets.QMainWindow = None, nonCriticalErrors: t.Tuple[_eType] = ()
    ):
        from .widgets import DialogHandler

        self.old_sys_excepthook = sys.excepthook
        self.addHandler(DialogHandler(logging.WARNING, win))
        self.nonCriticalErrors = nonCriticalErrors

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.excepthook = self.exceptWithLog

    def deregisterExceptions(self):
        sys.excepthook = self.old_sys_excepthook

    def registerWarnings(self):
        warnings.simplefilter("always", UserWarning)
        self.old_showwarning = warnings.showwarning
        warnings.showwarning = self.warnWithLog

    def warnWithLog(self, message, category, filename, lineno, file=None, line=None):
        """Copied logic from logging.captureWarnings implementation, but with short and long messages enabled"""
        if file is not None:
            if self.old_showwarning is not None:
                self.old_showwarning(message, category, filename, lineno, file, line)
        else:
            detailedMsg = warnings.formatwarning(
                message, category, filename, lineno, line
            )
            self.warning(message, extra={"detailed": detailedMsg})

    def exceptWithLog(self, etype, evalue, tb):
        # Allow sigabort to kill the app
        app = QtWidgets.QApplication.instance()
        if etype in [KeyboardInterrupt, SystemExit]:
            app.exit(1)
            app.processEvents()
            raise

        if issubclass(etype, self.nonCriticalErrors):
            level = PrjEnums.LOG_LVL_ATTN
        else:
            level = logging.CRITICAL
        self.log(level, "", exc_info=(etype, evalue, tb))

    @classmethod
    def getAppLogger(cls, name=""):
        """
        logging.getLogger only can spawn Logger classes, so this method includes a temporary override of the spawned
        class so that an AppLogger can be registered instead.
        """
        oldCls = logging.getLoggerClass()
        try:
            logging.setLoggerClass(cls)
            # False positive, logger class is overridden
            # noinspection PyTypeChecker
            logger: cls = logging.getLogger(name)
        finally:
            logging.setLoggerClass(oldCls)
        return logger


def makeExceptionsShowDialogs(
    win: QtWidgets.QMainWindow, nonCritErrs: t.Tuple[_eType] = (Warning,)
):
    """
    When a qt application encounters an error, it will generally crash the entire
    application even if this is undesirable behavior. This will make qt applications
    show a dialog rather than crashing.
    Use with caution! Maybe the application *should* crash on an error, but this will
    prevent that from happening.
    """
    warn(
        "This functionality is deprecated, please use an AppLogger with registerExceptionsToLogger instead",
        DeprecationWarning,
        stacklevel=2,
    )
    app = QtWidgets.QApplication.instance()
    from utilitys.widgets import ScrollableMessageDialog

    # Procedure taken from https://stackoverflow.com/a/40674244/9463643
    def new_except_hook(etype, evalue, tb):
        # Allow sigabort to kill the app
        if etype in [KeyboardInterrupt, SystemExit]:
            app.exit(1)
            app.processEvents()
            raise
        msgWithTrace = html.escape("".join(format_exception(etype, evalue, tb)))
        msgWithoutTrace = html.escape(str(evalue))
        dlg = ScrollableMessageDialog(
            win,
            notCritical=issubclass(etype, nonCritErrs),
            msgWithTrace=msgWithTrace,
            msgWithoutTrace=msgWithoutTrace,
        )
        dlg.show()
        dlg.exec_()

    def patch_excepthook():
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        global usingPostponedErrors
        sys.excepthook = new_except_hook
        usingPostponedErrors = True

    QtCore.QTimer.singleShot(0, patch_excepthook)
    app.processEvents()


def restoreExceptionBehavior():
    app = QtWidgets.QApplication.instance()

    def patch_excepthook():
        global usingPostponedErrors
        sys.excepthook = old_sys_except_hook
        usingPostponedErrors = False

    QtCore.QTimer.singleShot(0, patch_excepthook)
    app.processEvents()


def raiseErrorLater(err: Exception):
    warn(
        'This functionality is deprecated, please use an AppLogger.logLater("CRITICAL", ...) instead'
        " (or any other log level)",
        DeprecationWarning,
        stacklevel=2,
    )
    # Fire immediately if not in gui mode
    if not usingPostponedErrors:
        raise err
    # else
    def _raise():
        raise err

    QtCore.QTimer.singleShot(0, _raise)


def warnLater(msg: str, type_=Warning):
    warn(
        'This functionality is deprecated, please use an AppLogger.logLater("ATTN", ...) instead'
        " (or any other log level)",
        DeprecationWarning,
        stacklevel=2,
    )
    if not usingPostponedErrors:
        warn(msg, type_, stacklevel=2)
    else:
        QtCore.QTimer.singleShot(0, lambda: warn(msg, type_, stacklevel=2))


def pascalCaseToTitle(name: str, addSpaces=True) -> str:
    """
    Helper utility to turn a PascalCase name to a 'Title Case' title
    :param name: camel-cased name
    :param addSpaces: Whether to add spaces in the final result
    :return: Space-separated, properly capitalized version of :param:`Name`
    """
    if not name:
        return name
    replace = r" \1 "
    # changeROIImage -> change ROI Image
    # HTTPServer -> HTTP Server
    # exportData -> export Data
    name = re.sub(r"([A-Z]?[a-z0-9]+)", r" \1 ", name)
    name = name.replace("_", " ")
    # title() would turn HTTPS -> Https which we don't want
    parts = [p[0].upper() + p[1:] for p in name.split()]
    joiner = " " if addSpaces else ""
    return joiner.join(parts)


# Make a class for reference persistence
_nameFmtType = t.Callable[[str], str]


class NameFormatter:
    def __init__(self, formatter: t.Callable[[str], str] = pascalCaseToTitle):
        self._formatter = formatter

    def __call__(self, inStr: str):
        return self._formatter(inStr)

    @contextmanager
    def set(self, nameFmt: _nameFmtType):
        oldFmt = self._formatter
        self._formatter = nameFmt
        yield
        self._formatter = oldFmt


nameFormatter = NameFormatter()


def clsNameOrGroup(cls: t.Union[type, t.Any]):
    if not inspect.isclass(cls):
        cls = type(cls)
    if hasattr(cls, "__groupingName__"):
        return cls.__groupingName__
    return nameFormatter(cls.__name__)


def saveToFile(saveObj, savePath: FilePath, allowOverwriteDefault=False):
    savePath = Path(savePath)
    if not allowOverwriteDefault and savePath.stem.lower() == "default":
        errMsg = (
            "Cannot overwrite default setting.\n'Default' is automatically"
            " generated, so it should not be modified."
        )
        raise IOError(errMsg)
    else:
        # Known pycharm bug
        # noinspection PyTypeChecker
        with open(savePath, "w") as saveFile:
            yamlDump(saveObj, saveFile)


def attemptFileLoad(fpath: FilePath, openMode="r") -> t.Union[dict, bytes]:
    with open(fpath, openMode) as ifile:
        loadObj = yamlLoad(ifile)
    return loadObj


def clearUnwantedParamVals(paramState: dict):
    for _k, child in paramState.get("children", {}).items():
        clearUnwantedParamVals(child)
    if paramState.get("value", True) is None:
        paramState.pop("value")


def paramValues(param: Parameter, includeDefaults=False, includeKeys=()):
    """
    Saves just parameter values in a human readable fashion. Additional keys can be requested. If so, do not place
    `values` in this list, they will be included anyway
    """
    outDict = {}
    val = param.value()
    # Overloaded group parameters have no 'value' state, but do have children. Force this to
    # fall through to bottom block
    if includeDefaults or val != param.defaultValue() and not param.hasChildren():
        # Some values are not well represented as text, so call 'saveState' to ensure they work
        state = param.saveState()
        outDict[param.name()] = state["value"]

    if param.hasChildren() and (not outDict or includeDefaults):
        inner = {}
        for child in param:
            chState = paramValues(child, includeDefaults, includeKeys)
            inner.update(chState)
        if inner:
            outDict[param.name()] = inner
    return outDict


def paramDictWithOpts(
    param: Parameter,
    addList: t.List[str] = None,
    addTo: t.List[t.Type[Parameter]] = None,
    removeList: t.List[str] = None,
):
    """
    Allows customized alterations to which portions of a pyqtgraph parameter will be saved
    in the export. The default option only allows saving all or no extra options. This
    allows you to specify which options should be saved, and what parameter types they
    should be saved for.

    :param param: The initial parameter whose export should be modified
    :param addList: Options to include in the export for *addTo* type parameters
    :param addTo: Which parameter types should get these options
    :param removeList: Options to exclude in the export for *addTo* type parameters
    :return: Modified version of :paramDict: with alterations as explained above
    """
    if addList is None:
        addList = []
    if addTo is None:
        addTo = []
    if removeList is None:
        removeList = []

    def addCustomOpts(dictRoot, paramRoot: Parameter):
        for pChild in paramRoot:
            dChild = dictRoot["children"][pChild.name()]
            addCustomOpts(dChild, pChild)
        if type(paramRoot) in addTo:
            for opt in addList:
                if opt in paramRoot.opts:
                    dictRoot[opt] = paramRoot.opts[opt]
        for opt in removeList:
            if dictRoot.get(opt, True) is None:
                dictRoot.pop(opt)

    paramDict = param.saveState("user")
    addCustomOpts(paramDict, param)
    return paramDict


def applyParamOpts(param: Parameter, opts: dict):
    """Applies `opts` to `param` recursively. Used in place of pyqtgraph's implementation due to method connection errors"""
    state = opts.copy()
    childStates = state.pop("children", [])
    if isinstance(childStates, list):
        cs = {child["name"]: child for child in childStates}
        childStates = cs
    param.setOpts(**opts)
    for chName, chDict in childStates.items():
        if chName in param.names:
            applyParamOpts(param.child(chName), chDict)


def paramsFlattened(param: Parameter):
    addList = []
    if "group" not in param.type():
        addList.append(param)
    for child in param.children():  # type: Parameter
        addList.extend(paramsFlattened(child))
    return addList


def flexibleParamTree(
    treeParams: t.Union[t.List[Parameter], Parameter] = None,
    showTop=True,
    setTooltips=True,
    resizeNameCol=True,
):
    tree = ParameterTree()
    tree.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)
    tree.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
    if isinstance(treeParams, Parameter):
        treeParams = [treeParams]
    if not treeParams:
        treeParams = []
    # pyqtgraph bug: If tree isn't explicitly cleared, the inivisble root isn't configured correctly
    for param in treeParams:
        tree.addParameters(param, root=None, showTop=showTop)
    # def hookupSignals(p: Parameter):
    #   for ch in p:
    #     hookupSignals(ch)
    # Make wrapper out here to avoid lambda in loop scoping issues
    def hookupWrapper(param):
        def maybeUpdateTips(_param, change):
            desc = change[0][1]
            if "added" in desc.lower():
                setParamTooltips(tree)
                if resizeNameCol:
                    # Bug: Current 'resize to contents' makes the name column just a bit small
                    hint = tree.sizeHintForColumn(0)
                    tree.setColumnWidth(0, int(hint * 1.1))

        param.sigTreeStateChanged.connect(maybeUpdateTips)

    if setTooltips:
        for param in treeParams:
            hookupWrapper(param)
        setParamTooltips(tree)
    # hookupSignals(topParam)
    return tree


def setParamsExpanded(tree: ParameterTree, expandedVal=True):
    for item in tree.topLevelItems():
        for ii in range(item.childCount()):
            item.child(ii).setExpanded(expandedVal)
    tree.resizeColumnToContents(0)


def forceRichText(text: str):
    """
    Wraps text in <qt> tags to make Qt treat it as rich text. Since tooltips don't wrap nicely unless text is rich,
    this ensures all encountered tooltips are correctly wrapped.

    :param text: text, may already start with <qt> tags
    """
    if "PySide" in QT_LIB:
        richDetect = QtGui.Qt.mightBeRichText
    else:
        richDetect = QtCore.Qt.mightBeRichText
    if richDetect(text):
        return text
    return f"<qt>{text}</qt>"


def setParamTooltips(tree: ParameterTree, expandNameCol=False):
    iterator = QtWidgets.QTreeWidgetItemIterator(tree)
    item: QtWidgets.QTreeWidgetItem = iterator.value()
    while item is not None:
        # TODO: Set word wrap on long labels. Currently either can show '...' or wrap but not
        #   both
        # if tree.itemWidget(item, 0) is None:
        #   lbl = QtWidgets.QLabel(item.text(0))
        #   tree.setItemWidget(item, 0, lbl)
        if (
            hasattr(item, "param")
            and "tip" in item.param.opts
            and len(item.toolTip(0)) == 0
            and tree.itemWidget(item, 0) is None
        ):
            item.setToolTip(0, forceRichText(item.param.opts["tip"]))
        iterator += 1
        item = iterator.value()
    if expandNameCol:
        setParamsExpanded(tree, True)


def resolveYamlDict(cfgFname: FilePath, cfgDict: dict = None):
    if cfgDict is not None:
        cfg = cfgDict
    else:
        cfg = attemptFileLoad(cfgFname)
        if cfg is None:
            # Empty file
            cfg = {}
    if cfgFname is not None:
        cfgFname = Path(cfgFname)
    return cfgFname, cfg


def getParamChild(
    param: Parameter,
    *childPath: t.Sequence[str],
    allowCreate=True,
    groupOpts: dict = None,
    chOpts: dict = None,
):
    if groupOpts is None:
        groupOpts = {}
    groupOpts.setdefault("type", "group")
    while childPath and childPath[0] in param.names:
        param = param.child(childPath[0])
        childPath = childPath[1:]
    # All future children must be created
    if allowCreate:
        for chName in childPath:
            param = param.addChild(dict(name=chName, **groupOpts))
            childPath = childPath[1:]
    elif len(childPath) > 0:
        # Child doesn't exist
        raise KeyError(f"Children {childPath} do not exist in param {param}")
    if chOpts is not None:
        if chOpts["name"] in param.names:
            param = param.child(chOpts["name"])
        else:
            param = param.addChild(chOpts)
    if not param.hasDefault():
        param.setDefault(param.value())
    return param


class ArgParseConverter(argparse.ArgumentParser):
    """Able to convert arguments to their types on parse_args"""

    convertRemainder = True

    @staticmethod
    def argConverter(arg, returnSuccess=False):
        try:
            ret = ast.literal_eval(arg)
            success = True
        except:
            ret = arg
            success = False
        if returnSuccess:
            return ret, success
        return ret

    def _get_value(self, action, arg_string: str) -> t.Any:
        ret, success = self.argConverter(arg_string, returnSuccess=True)
        if not success:
            return super()._get_value(action, arg_string)
        return ret

    @classmethod
    def _lookAheadForValue(cls, extraIter, ii):
        try:
            nextK = extraIter[ii + 1]
            if nextK.startswith("--"):
                # This is also a flag condition, don't consume value this round
                vv = True
            else:
                vv = cls.argConverter(nextK)
                # Value consumed, move on an extra space
                ii += 1
        except IndexError:
            vv = True
        return vv, ii

    @classmethod
    def _consumeNextIterPos(cls, extraIter, ii):
        item = extraIter[ii]
        kk = vv = None
        if not item.startswith("--"):
            return kk, vv, ii + 1
        kk = item.strip("--")
        if "=" in kk:
            # Don't consume next key, this is the value
            kk, toParse = kk.split("=", 1)
            vv = cls.argConverter(toParse)
        else:
            vv, ii = cls._lookAheadForValue(extraIter, ii)
        return kk, vv, ii + 1

    def parse_args(self, args=None, namespace=None):
        namespace, args = super().parse_known_args(args, namespace)
        # Treat remainder as if they belonged
        named = vars(namespace)
        if not self.convertRemainder:
            return namespace
        extraIter = list(args)
        ii = 0
        while ii < len(extraIter):
            kk, vv, ii = self._consumeNextIterPos(extraIter, ii)
            if kk is not None:
                named[kk] = vv
        return Namespace(**named)


def makeCli(
    func: t.Callable, convertArgs=True, parserKwargs: dict = None, **procKwargs
):
    """
    Creates a CLI interface to a function from the provided function, parsing the documentation for help text, signature
    for default values, etc.

    :param func: Function from which to make a CLI interface
    :param convertArgs: Whether to use a parser which converts string cli arguments to python values
    :param parserKwargs: Passed to ArgumentParser on init
    :param procKwargs: Passed to AtomicProcess which is used as an intermediate to generate parameter documentation
    """
    from ._funcparse import funcToParamDict, RunOpts

    def tipConverter(inStr):
        doc = QtGui.QTextDocument()
        doc.setHtml(inStr)
        return doc.toPlainText()

    funcDict = funcToParamDict(func, **procKwargs)
    tip = funcDict.get("func-description", "")

    useCls = argparse.ArgumentParser if not convertArgs else ArgParseConverter
    parserKwargs = parserKwargs or {}
    parserKwargs.setdefault("description", tipConverter(tip))
    parser = useCls(**parserKwargs)

    for ch in funcDict["children"]:
        if "action" in ch["type"]:
            continue
        arg = parser.add_argument(
            f'--{ch["name"]}', required=ch["value"] is RunOpts.PARAM_UNSET
        )
        if not arg.required:
            chType = type(ch["value"])
            if ch["value"] is not None:
                arg.type = type(ch["value"])
            arg.default = ch["value"]
        if "tip" in ch:
            arg.help = tipConverter(ch["tip"])
    # if proc.hasKwargs:
    #   sig = inspect.signature(func)
    #   kwParam = [name for name, par in sig.parameters.items() if par.kind is par.VAR_KEYWORD][0]
    #   parser.add_argument(f'--{kwParam}', nargs=argparse.REMAINDER, dest=argparse.SUPPRESS)
    return parser


def dialogGetSaveFileName(parent, winTitle, defaultTxt: str = None) -> t.Optional[str]:
    failedSave = True
    returnVal: t.Optional[str] = None
    while failedSave:
        saveName, ok = QtWidgets.QInputDialog().getText(
            parent, winTitle, winTitle + ":", QtWidgets.QLineEdit.Normal, defaultTxt
        )
        # TODO: Make this more robust. At the moment just very basic sanitation
        for disallowedChar in ["/", "\\"]:
            saveName = saveName.replace(disallowedChar, "")
        if ok and not saveName:
            # User presses 'ok' without typing anything except disallowed characters
            # Keep asking for a name
            continue
        elif not ok:
            # User pressed 'cancel' -- Doesn't matter whether they entered a name or not
            # Stop asking for name
            break
        else:
            # User pressed 'ok' and entered a valid name
            return saveName
    return returnVal


def paramWindow(param: Parameter, modal=True, exec=True):
    tree = flexibleParamTree(param)
    setParamsExpanded(tree, True)
    dlg = QtWidgets.QDialog()
    layout = QtWidgets.QVBoxLayout()
    dlg.setLayout(layout)
    dlg.setModal(modal)
    layout.addWidget(tree)
    # Show before exec so size calculations are correct, and fix the height by a small factor
    dlg.show()
    dlg.resize(dlg.width(), dlg.height() + 25)
    if exec:
        dlg.exec_()


def hookupParamWidget(param: Parameter, widget):
    """
    Parameter widgets created outside param trees need to have their sigChanging, sigChanged, etc. signals hooked up to
    the parameter itself manually. The relevant code below was extracted from WidgetParameterItem
    """

    def widgetValueChanged():
        val = widget.value()
        return param.setValue(val)

    def paramValueChanged(param, val, force=False):
        if force or not pg.eq(val, widget.value()):
            try:
                widget.sigChanged.disconnect(widgetValueChanged)
                param.sigValueChanged.disconnect(paramValueChanged)
                widget.setValue(val)
                param.setValue(widget.value())
            finally:
                widget.sigChanged.connect(widgetValueChanged)
                param.sigValueChanged.connect(paramValueChanged)

    param.sigValueChanged.connect(paramValueChanged)
    if widget.sigChanged is not None:
        widget.sigChanged.connect(widgetValueChanged)

    if hasattr(widget, "sigChanging"):
        widget.sigChanging.connect(
            lambda: param.sigValueChanging.emit(param, widget.value())
        )

    ## update value shown in widget.
    opts = param.opts
    if opts.get("value", None) is not None:
        paramValueChanged(param, opts["value"], force=True)
    else:
        ## no starting value was given; use whatever the widget has
        widgetValueChanged()


def popupFilePicker(
    parent=None,
    winTitle: str = "",
    fileFilter: str = "",
    existing=True,
    asFolder=False,
    selectMultiple=False,
    startDir: str = None,
    **kwargs,
) -> t.Optional[t.Union[str, t.List[str]]]:
    """
    Thin wrapper around Qt file picker dialog. Used internally so all options are consistent
    among all requests for external file information

    :param parent: Dialog parent
    :param winTitle: Title of dialog window
    :param fileFilter: File filter as required by the Qt dialog
    :param existing: Whether the file is already existing, or is being newly created
    :param asFolder: Whether the dialog should select folders or files
    :param selectMultiple: Whether multiple files can be selected. If `asFolder` is
      *True*, this parameter is ignored.
    :param startDir: Where in the file system to open this dialog
    :param kwargs: Consumes additional arguments so dictionary unpacking can be used
      with the lengthy file signature. In the future, this may allow additional config
      options.
    """
    fileDlg = QtWidgets.QFileDialog(parent)
    fileMode = fileDlg.AnyFile
    opts = fileDlg.DontUseNativeDialog
    if existing:
        # Existing files only
        fileMode = fileDlg.ExistingFiles if selectMultiple else fileDlg.ExistingFile
    else:
        fileDlg.setAcceptMode(fileDlg.AcceptSave)
    if asFolder:
        fileMode = fileDlg.Directory
        opts |= fileDlg.ShowDirsOnly
    fileDlg.setFileMode(fileMode)
    fileDlg.setOptions(opts)
    fileDlg.setModal(True)
    if startDir is not None:
        fileDlg.setDirectory(startDir)
    fileDlg.setNameFilter(fileFilter)

    fileDlg.setOption(fileDlg.DontUseNativeDialog, True)
    fileDlg.setWindowTitle(winTitle)

    if fileDlg.exec_():
        # Append filter type
        singleExtReg = r"(\.\w+)"
        # Extensions of type 'myfile.ext.is.multi.part' need to capture repeating pattern of singleExt
        suffMatch = re.search(rf"({singleExtReg}+)", fileDlg.selectedNameFilter())
        if suffMatch:
            # Strip leading '.' if it exists
            ext = suffMatch.group(1)
            if ext.startswith("."):
                ext = ext[1:]
            fileDlg.setDefaultSuffix(ext)
        fList = fileDlg.selectedFiles()
    else:
        fList = []

    if selectMultiple:
        return fList
    elif len(fList) > 0:
        return fList[0]
    else:
        return None


def hierarchicalUpdate(
    curDict: dict, other: dict, replaceLists=False, uniqueListElements=False
):
    """Dictionary update that allows nested keys to be updated without deleting the non-updated keys"""
    if other is None:
        return curDict
    for k, v in other.items():
        curVal = curDict.get(k)
        if isinstance(curVal, dict) and isinstance(v, dict):
            hierarchicalUpdate(curVal, v, replaceLists, uniqueListElements)
        elif not replaceLists and isinstance(curVal, list) and isinstance(v, list):
            if uniqueListElements:
                v = [el for el in v if el not in curVal]
            curVal.extend(v)
        else:
            curDict[k] = v
    return curDict


def timedExec(
    updateFunc: t.Union[t.Generator, t.Callable],
    interval_ms: int,
    argLst: t.Sequence = None,
    stopCond: t.Callable = None,
):
    """
    Iterates over an argument list (or generator) and executes the next action every
    `interval_ms` ms. Useful for updating GUI elements periodically, e.g. showing a list
    of images one at a time. Set `interval_ms` to <= 0 to avoid starting right away.
    """
    timer = QtCore.QTimer()
    if argLst is None:
        # updateFunc must be a generator
        argLst = updateFunc()
        updateFunc = lambda arg: None
    if stopCond is None:
        stopCond = lambda: False
    argLst = iter(argLst)

    def update():
        if stopCond():
            timer.stop()
        try:
            arg = next(argLst)
            updateFunc(arg)
        except StopIteration:
            timer.stop()

    timer.timeout.connect(update)
    if interval_ms > 0:
        timer.start(interval_ms)
    return timer


def gracefulNext(generator: t.Generator):
    try:
        return next(generator)
    except StopIteration as ex:
        return ex.value


def readDataFrameFiles(
    folder: FilePath,
    readFunc: t.Callable,
    globExpr="*.*",
    concatKwargs: dict = None,
    **readKwargs,
):
    """
    Reads files in a folder and concatenates them into one output dataframe

    :param folder: Folder to find files
    :param readFunc: Read function to use, must take file and ``readArgs`` to produce a dataframe.
    :param globExpr: Optionally filter for specific files in ``folder`` by altering the glob expression
    :param concatArgs: Dict of keywords passed to ``pd.concat``
    :param readArgs: Passed to readFunc for each encountered file
    """
    files = naturalSorted(Path(folder).glob(globExpr))
    dfs = [readFunc(file, **readKwargs) for file in files]
    return pd.concat(dfs, **(concatKwargs or {}))


def naturalSorted(iterable):
    """
    Copied from tiffile implementation, but works with non-string objects (e.g. Paths)

    >>> natural_sorted(['f1', 'f2', 'f10'])
    ['f1', 'f2', 'f10']

    """

    def sortkey(x):
        x = str(x)
        return [(int(c) if c.isdigit() else c) for c in re.split(numbers, x)]

    numbers = re.compile(r"(\d+)")
    return sorted(iterable, key=sortkey)


class DummySignal:
    """Useful for spoofing a qt connection that doesn't do anything"""

    def connect(self, *args):
        pass

    def disconnect(self, *args):
        pass

    def emit(self, *args):
        if self.capture:
            self.emissions.append(args)

    def __init__(self, capture=False):
        self.emissions = []
        self.capture = capture


@contextmanager
def makeDummySignal(obj, sigName: str, capture=False):
    oldSig = getattr(obj, sigName)
    try:
        newSig = DummySignal(capture)
        setattr(obj, sigName, newSig)
        yield newSig
    finally:
        setattr(obj, sigName, oldSig)


def getAnyPgColormap(name, forceExist=False):
    """
    Pyqtgraph allows file, matplotlib, or colorcet cmaps but doesn't allow getting from
    an arbitrary source. This simply shims access to ``pg.colormap.get`` which tries
    all sources each time a source-specific ``get`` fails.
    :param name: passed to ``pg.colormap.get``
    :param forceExist: If *True*, the function will raise an error instead of returning
        *None* if the name was not found.
    """
    for source in None, "matplotlib", "colorcet":
        try:
            cmap = pg.colormap.get(name, source=source)
        except FileNotFoundError:
            # For None source when local file doesn't exist
            cmap = None
        if cmap is not None:
            return cmap
    # cmap = None at this point
    if forceExist:
        raise ValueError(
            f"'{name}' was not recognized among the available"
            f" options. Must be one of:\n{fns.listAllPgColormaps()}"
        )
    # else
    return None


def listAllPgColormaps():
    """``Shims pg.colormap.listMaps`` to list all colormaps (i.e. for all sources)"""
    maps = []
    for source in None, "matplotlib", "colorcet":
        nextMaps = pg.colormap.listMaps(source)
        for curMap in nextMaps:
            if curMap not in maps:
                maps.append(curMap)
    return maps
