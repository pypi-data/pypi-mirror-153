from .prjparam import PrjParam
from .parameditor import *
from .shortcut import ShortcutsEditor
from .pgregistered import ShortcutParameter
from .procwrapper import NestedProcWrapper
from .plugin import dockPluginFactory, ParamEditorPlugin
from .. import fns

from .._funcparse import RunOpts

RunOpts.defaultCfg["title"] = fns.nameFormatter
