from __future__ import annotations

import contextlib
from contextlib import ExitStack

import copy
import copy as _copy
import inspect
import pickle
import typing as t
from abc import ABC
from collections.abc import MutableMapping
from functools import wraps
from warnings import warn

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.Parameter import PARAM_TYPES

from ._funcparse import funcToParamDict, RunOpts
from .fns import nameFormatter, makeDummySignal

__all__ = [
    "ProcessIO",
    "ProcessStage",
    "NestedProcess",
    "AtomicProcess",
    "ParamContainer",
]


_infoType = t.List[t.Union[t.List, t.Dict[str, t.Any]]]
StrList = t.List[str]
StrCol = t.Collection[str]


class ParamContainer(MutableMapping):
    """
    Utility for exposing dict-like behavior to the user for inserting and querying parameter objects. Behaves amost
    like a pyqtgraph parameter, with the exception that new parameter "children" can be added through the dict
    interface
    """

    def __init__(self, **kwargs):
        self.params = {}
        self.extras = {}
        for name, value in kwargs.items():
            self[name] = value

    def __delitem__(self, key):
        if key in self.extras and key in self.params:
            raise KeyError(f"Key {key} is ambiguous, exists in both extras and params")
        try:
            self.extras.__delitem__(key)
        except KeyError:
            # Keyerror on non existence will be raised in the except block
            self.params.__delitem__(key)

    def __iter__(self):
        for d in self.extras, self.params:
            yield from d

    def __len__(self):
        return self.params.__len__() + self.extras.__len__()

    def __setitem__(self, key, value):
        if isinstance(value, Parameter):
            self.params[key] = value
        elif key in self.params:
            self.params[key].setValue(value)
        else:
            self.extras[key] = value

    def __getitem__(self, item):
        try:
            return self.extras[item]
        except KeyError:
            return self.params[item].value()

    def copy(self, deepCopyParams=True, deepCopyExtras=False, deepCopyAttrs=False):
        ret = type(self)()
        ret.__dict__.update(self.__dict__)
        # Will be filled in later
        ret.extras = {}
        ret.params = {}
        if deepCopyAttrs:
            ret.__dict__ = copy.deepcopy(ret.__dict__)

        if deepCopyExtras:
            ret.extras = copy.deepcopy(self.extras)
        else:
            ret.extras = self.extras.copy()
        # As of now, ret.copy()['param'] = value will still modify ret['param'] if `deepCopyParams` is false.
        # Sometimes this may be desired, but doesn't follow the interface of dict.copy()['key'] = value preventing
        # modification of the original dict's key
        if deepCopyParams:
            for param, val in self.params.items():
                ret.params[param] = Parameter.create(**val.saveState())
        else:
            ret.params = self.params.copy()
        return ret

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memodict):
        return self.copy(deepCopyExtras=True, deepCopyAttrs=True)

    def __str__(self):
        pieces = []
        for subdict, title in zip([self.extras, self.params], ["Extra", "Params"]):
            if len(subdict):
                pieces.append(f"{title}: {subdict}")
            else:
                pieces.append(f"{title}: <No keys>")
        return "\n".join(pieces)

    def __repr__(self):
        return str(self)


class ProcessIO(ParamContainer):
    """
    The object through which the processor pipeline communicates data. Inputs to one process
    become updated by the results from that process, and this updated ProcessIO is used
    as the input to the *next* process.
    """

    FROM_PREV_IO = RunOpts.PARAM_UNSET
    """
  Helper class to indicate whether a key in this IO is supposed to come from
  a previous process stage. Typical usage:
  ```if not hyperparam: self[k] = self.FROM_PREV_IO```

  Typically, process objects will have two IO dictionaries: One that hold the input spec
  (which makes use of `FROM_PREV_IO`) and one that holds the runtime process values. The
  latter IO will not make use of `FROM_PREV_IO`.
  """

    def __init__(self, hyperParamKeys: t.List[str] = None, **kwargs) -> None:
        """
        :param hyperParamKeys: Hyperparameters for this process that aren't expected to come
          from the previous stage in the process. Forwarded keys (that were passed from a
          previous stage) are inferred by everything that is not a hyperparameter key.
        :param kwargs: see *dict* init
        """
        if hyperParamKeys is None:
            hyperParamKeys = []
        self.hyperParamKeys = hyperParamKeys
        warnKeys = []
        for k in self.hyperParamKeys:
            if k not in kwargs:
                warnKeys.append(k)
                kwargs[k] = None
        if warnKeys:
            warn(
                f"Hyperparameter keys were specified, but did not exist in provided"
                f" inputs:\n{warnKeys}\n"
                f"Defaulting to `None` for those keys.",
                UserWarning,
            )
        super().__init__(**kwargs)
        self.keysFromPrevIO = {k for (k, v) in self.items() if v is self.FROM_PREV_IO}
        self.hasKwargs = False

    @classmethod
    def fromFunction(
        cls,
        func: t.Callable,
        ignoreKeys: StrCol = None,
        interactive=True,
        **overriddenDefaults,
    ):
        """
        In the ProcessIO scheme, default arguments in a function signature constitute algorithm
        hyperparameters, while required arguments must be provided each time the function is
        run. If `**overriddenDefaults` is given, this will override any default arguments from
        `func`'s signature.
        :param func: Function whose input signature should be parsed
        :param ignoreKeys: Keys to disregard entirely from the incoming function. This is useful for cases like adding
          a function at the class instead of instance level and `self` shouldn't be regarded by the parser.
        :param interactive: Whether pyqtgraph parameters should be created to interact with each hyperparameter
        :param overriddenDefaults: Keys here that match default argument names in `func` will
          override those defaults. If an argument does _not_ have a default in the function definition but should
          be shown to the user, provide a default here and it will appear.
        """
        # Add custom kwarg to test for **kwarg presence
        overriddenDefaults["test for kwargs"] = True
        overriddenDefaults.setdefault("title", nameFormatter)
        funcDict = funcToParamDict(func, **overriddenDefaults)

        outDict = {ch["name"]: ch for ch in funcDict["children"]}
        if ignoreKeys is None:
            ignoreKeys = []
        for kk in ignoreKeys:
            if kk not in overriddenDefaults:
                outDict.pop(kk, None)

        values = [ch["value"] for ch in outDict.values()]
        ignores = [ch.get("ignore", False) for ch in outDict.values()]
        if not interactive:
            # Recycle values only
            outDict = dict(zip(outDict, values))

        hasKwargs = outDict.pop("test for kwargs", False)
        hyperParamKeys = []
        for ii, (name, child) in enumerate(outDict.items()):
            # Unrepresentable parameters should be turned back into raw values
            val = values[ii]
            isHyperparam = (
                val is not RunOpts.PARAM_UNSET
                and name not in ignoreKeys
                and not ignores[ii]
            )
            if not isHyperparam or (interactive and child["type"] not in PARAM_TYPES):
                outDict[name] = val
            elif isHyperparam:
                hyperParamKeys.append(name)

        cls._aliasOverlappingArgs(outDict)

        if interactive:
            for param in hyperParamKeys:
                outDict[param] = Parameter.create(**outDict[param])
        out = cls(hyperParamKeys, **outDict)
        out.hasKwargs = hasKwargs
        return out

    @classmethod
    def _aliasOverlappingArgs(cls, paramDict):
        """
        Alias arguments in paramDict by prefixing underscores if they conflict with ProcessIO keywords. This allows
        functions with the same keywords as ProcessIO to still forward them to the inner input dictionary
        """
        initSig = inspect.signature(cls.__init__).parameters
        keys = list(paramDict)
        for key in keys:
            if key in initSig:
                newName = "_" + key
                paramDict[newName] = paramDict[key]
                del paramDict[key]


class ProcessStage(ABC):
    name: str
    input: ProcessIO = None
    allowDisable = False
    disabled = False
    cacheOnDisable = False
    result: t.Optional[ProcessIO] = None
    inMap: t.Union[t.List[str], t.Dict[str, str]] = None
    outMap: t.Union[t.List[str], t.Dict[str, str]] = None
    nameForState = None
    """
  Can be overridden to appear as a different heading in a saved state. This is useful when e.g. loading a state
  from its fully qualified (+ module) name. Should be overridden at the instance level
  """

    class _DUPLICATE_INFO:
        pass

    """Identifies information that is the same in two contiguous stages"""

    def __repr__(self) -> str:
        selfCls = type(self)
        oldName: str = super().__repr__()
        # Remove module name for brevity
        oldName = oldName.replace(
            f"{selfCls.__module__}.{selfCls.__name__}",
            f"{selfCls.__name__} '{self.name}'",
        )
        return oldName

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: NestedProcess):
        if not isinstance(other, NestedProcess):
            return False
        try:
            return pg.eq(self.saveState(True, True), other.saveState(True, True))
        except TypeError:
            # Default to false for types not comparable by pyqtgraph
            return False

    def __hash__(self):
        return id(self)

    def updateInput(self, prevIo: ProcessIO = None, allowExtra=False, **kwargs):
        """
        Helper function to update current inputs from previous ones while ignoring leading
        underscores.

        :param prevIo: Io object to forward updated inputs here. Extra inputs can be supplied to **kwargs
        :param allowExtra: Whether to allow setting of keys that didn't exist in the original input. This can be valid
          in the case where the underlying function accepts **kwargs
        """
        raise NotImplementedError

    def run(self, io: ProcessIO = None, disable=False, **runKwargs):
        raise NotImplementedError

    def __call__(self, **kwargs):
        return self.run(ProcessIO(**kwargs))

    def __iter__(self):
        raise NotImplementedError

    def saveState(self, includeDefaults=False, includeMeta=False):
        """
        Serializes the process' state in terms of its composition and inputs.

        :param includeDefaults: Whether to also serialize inputs that are unchanged from the original process creation
        :param includeMeta: Whether to also serialize metadata about the stage such as its disable/allowDisable status
        """
        raise NotImplementedError

    def saveStateFlattened(self, includeDefault=False, includeMeta=False):
        """Saves state while collapsing all nested processes into one list of atomic processes"""
        return self.saveState(includeDefault, includeMeta)

    def saveMetaProps(self, **filterOpts):
        """
        Converts a saved state of parameters and staegs to one including disabled and allowDisable statuses

        :param filterOpts: Values to ignore if they match. So, passing `disabled=True` will only
          record the `disabled` property if it is *False*. This is an easy way of ignoring default properties. Setting a key
          to *None* will ignore that property entirely.
        """
        metaProps = ("allowDisable", "disabled", "inMap", "outMap")

        class UNSET:
            pass

        # Convert back if no props were added
        out = {}
        for k in metaProps:
            selfVal = getattr(self, k)
            cmp = filterOpts.get(k, UNSET)
            if (
                cmp is None
                or pg.eq(cmp, selfVal)
                or pg.eq(getattr(type(self), k, UNSET), selfVal)
            ):
                continue
            out[k] = selfVal
        return out

    def addMetaProps(self, state: t.Union[dict, str], **metaFilterOpts):
        """
        Helper method to insert meta properties into the current state. Since the state might be a string, or meta props
        might be empty, this performs checks to ensure only the most simplified output form is preserved
        """
        state = _copy.copy(state)
        metaProps = self.saveMetaProps(**metaFilterOpts)
        if not metaProps:
            return state
        if isinstance(state, str):
            state = {state: {}}
        state.update(metaProps)
        return state


class AtomicProcess(ProcessStage):
    """
    Often, process functions return a single argument (e.g. string of text,
    processed image, etc.). In these cases, it is beneficial to know what name should
    be assigned to that result.
    """

    def __init__(
        self,
        func: t.Callable,
        name: str = None,
        *,
        inMap=None,
        outMap=None,
        wrapWith=None,
        docFunc: t.Callable = None,
        **procIoKwargs,
    ):
        """
        :param func: Function to wrap
        :param name: Name of this process. If `None`, defaults to the function name with
          camel case or underscores converted to title case.
        :param wrapWith: For functions not defined by the user, it is often inconvenient if they have
        to be redefined just to return a ProcessIO object. If `func` does not return a `ProcessIO`
        object, `wrapWith` can be set to the desired output keys. In this case, `func` is assumed to
        returns either one result or a list of results. It is converted into a function
        returning a ProcessIO object instead. Each `wrapWith` key is assigned to each output
        of the function in order. If only one wrap key exists, then the output of the
        function is assumed to be that key. I.e. in the case where `len(cls.inMap) == 1`,
        the output is expected to be the direct result, not a sequence of results per key.
        :param inMap: Method of mapping inputs from a previous process into inputs consumable by this one. Dict in the form
          of {outKey: inExpr}, where inExpr is any valid python expression consisting only of expected inputs from a previous
          process. If *None*, no mapping is performed.
        :param outMap: See `inMap`. This is the same concept, but maps as {exposed: resultExpr}, where exposed is what
          processes after this see, and resultExpr is some expression based just on results from the function eval.
        :param docFunc: Sometimes, `func` is a wrapper around a different function, where this other function is what should
          determine the created user parameters. In these cases (i.e. one function directly calling another), that inner
          function can be provided here for parsing the docstring and parameters. This is only used for the purpose of
          creationg a function specification and is ignored afterward.
        :param procIoKwargs: Passed to ProcessIO.fromFunction
        """
        if name is None:
            name = nameFormatter((docFunc or func).__name__)
        self.inMap = inMap or self.inMap
        self.outMap = outMap or self.outMap

        self.cacheOnEq = True
        """Whether equal inputs should result in a cached output rather than recomputing"""

        self.name = name
        try:
            self.input = ProcessIO.fromFunction(docFunc or func, **procIoKwargs)
        except ValueError:
            # Happens on builtins / c-defined functions. Assume user passes all meaningful args at startup
            self.input = ProcessIO(**procIoKwargs)
            self.input.hyperParamKeys = {
                k for k, v in self.input.items() if v is not None
            }
        self.hasKwargs = self.input.hasKwargs
        self.result: t.Optional[ProcessIO] = None
        # If the input changes but no process is run, make sure this doesn't change what the input for the last result
        # was
        self.inputForResult: dict = None
        self.fnDoc = (docFunc or func).__doc__
        """Record function documentation of proxy if needed so wrapper functions properly"""

        if self.inMap is not None:
            keys = set(self.input.keys())
            missingKeys = set(self.inMap) - keys
            if missingKeys:
                raise KeyError(
                    f"{name} input signature is missing the following required input keys:\n"
                    f"{missingKeys}"
                )

        if wrapWith is not None:
            func = self._wrappedFunc(func, wrapWith)
        self.func = func
        self.defaultInput = copy.deepcopy(self.input)

    @classmethod
    def _wrappedFunc(cls, func, mainResultKeys: StrList):
        """
        Wraps a function returining either a result or list of results, instead making the
        return value an `FRProcessIO` object where each `cls.mainResultkey` corresponds
        to a returned value
        """
        if len(mainResultKeys) == 1:

            @wraps(func)
            def newFunc(*args, **kwargs):
                return ProcessIO(**{mainResultKeys[0]: func(*args, **kwargs)})

        else:

            @wraps(func)
            def newFunc(*args, **kwargs):
                return ProcessIO(
                    **{k: val for k, val in zip(mainResultKeys, func(*args, **kwargs))}
                )

        return newFunc

    def _maybeWrapStageFunc(self, oldresult: t.Any):
        """
        It is not possible to determine what value type is returned until a stage is first run. For cases in which this
        result is *not* a ProcessIO object, but one is required for mapping / pipelining, this function both wraps the
        old result in a ProcessIO object *and* wraps the atomic function so all future results are also ProcessIO objects.
        If this process fails, nothing happens to the stage's function
        """
        oldFunc = self.func
        useKeys = list(self.outMap)
        try:
            self.func = self._wrappedFunc(oldFunc, useKeys)
            # Capture current result as a process io
            def dummyFunc():
                return oldresult

            oldresult = self._wrappedFunc(dummyFunc, useKeys)()
        except Exception as ex:
            # Many things can go wrong, safely revert
            warn(
                f"Tried to convert outputs for process {self.name} into a ProcessIO"
                f" but this failed with the following error:\n"
                f"{ex}",
                UserWarning,
            )
            self.func = oldFunc
        return oldresult

    @property
    def keysFromPrevIO(self):
        return self.input.keysFromPrevIO

    def run(self, io: ProcessIO = None, disable=False, **runKwargs):
        disable = disable or self.disabled
        stack = ExitStack()
        # Avoid parameter updates here from re-triggering a run by temporarily removing their changing signals
        try:
            for param in set(runKwargs).union(io or {}).intersection(self.input.params):
                for sig in "sigValueChanged", "sigValueChanging":
                    stack.enter_context(makeDummySignal(self.input.params[param], sig))
            self.updateInput(io, **runKwargs)
        finally:
            stack.close()
        missingInputs = [
            f'"{kk}"'
            for (kk, vv) in self.input.items()
            if vv is self.input.FROM_PREV_IO
        ]
        if len(missingInputs):
            raise KeyError(
                f'Missing one or more required inputs: {", ".join(missingInputs)}'
            )
        try:
            # Use dicts instead of raw ProcessIO objects since pg params should
            # be converted to values before comparison
            cmp = self.cacheOnEq and pg.eq(self.inputForResult, dict(self.input))
        except Exception as ex:
            # Thrown exception is broad on pg equality comparison, so check the message
            strEx = str(ex)
            if "==" in strEx or "failed to evaluate equivalence" in strEx:
                cmp = False
            else:
                raise

        if cmp and self.result is not None and not disable:
            # Hypothetically the result should be the same
            return self.result
        if not disable:
            out = self.func(**self.input)
            if self.outMap and not isinstance(out, ProcessIO):
                out = self._maybeWrapStageFunc(out)
            self.result = self.computeArgMapping(self.outMap, out)
            self.inputForResult = dict(self.input)
        elif not self.cacheOnDisable:
            self.result = self.inputForResult = None
        out = self.result
        if out is None:
            out = self.input
        return out

    def computeArgMapping(
        self,
        mapping: t.Union[t.Dict[str, str], t.Sequence[str]],
        toMap: dict,
        copy=True,
    ):
        """
        Converts toMap into outputs by rules specified in mapping. e.g. if mapping was {in: out + 5} then `toMap` is searched
        for "out", the expression is evaluated, and the result is assigend to key "in" in the output.
        If `mapping` is a sequence instead of dict, those are considered keys in the preferred order. *copy* determines
        whether the pre-mapped values should all be copied into the result, where keys present in mapping will be overridden
        """
        if mapping is None:
            return toMap
        out = toMap.copy() if copy else {}
        if isinstance(mapping, t.Sequence):
            return ProcessIO(**{kk: toMap[kk] for kk in mapping})
        # Eval needs dict
        toMap = dict(toMap)
        for kk, expr in mapping.items():
            out[kk] = eval(expr, toMap)
        return ProcessIO(**out)

    def updateInput(self, prevIo: ProcessIO = None, allowExtra=False, **kwargs):
        allowExtra = allowExtra or self.hasKwargs
        if prevIo is None:
            prevIo = ProcessIO()
        useIo = prevIo.copy()
        useIo.update(kwargs)
        useIo = self.computeArgMapping(self.inMap, useIo)
        selfFmtToUnfmt = {k.lstrip("_"): k for k in self.input}
        prevIoKeyToFmt = {k.lstrip("_"): k for k in {**useIo}}
        setKeys = set()
        for fmtK, value in zip(prevIoKeyToFmt, useIo.values()):
            if fmtK in selfFmtToUnfmt:
                trueK = selfFmtToUnfmt[fmtK]
                self.input[trueK] = value
                setKeys.add(fmtK)
            elif allowExtra:
                # No true key already exists, so assume formatting leads to desired name
                self.input[fmtK] = value
                # Not possible for this to be required, so no need to add to set keys

    def saveState(self, includeDefaults=False, includeMeta=False, **metaFilterOpts):
        def keepCond(k, v):
            # Can fail with unsavable types (e.g. numpy arrays)
            # TODO: Determine appropriate response
            # noinspection PyBroadException
            try:
                return (
                    (k in self.input.hyperParamKeys or k not in self.defaultInput)
                    and (includeDefaults or not pg.eq(v, self.defaultInput.get(k)))
                    and v is not self.input.FROM_PREV_IO
                )
            except Exception:
                return False

        saveIo = {k: v for k, v in self.input.items() if keepCond(k, v)}
        saveName = self.nameForState or self.name
        if not saveIo:
            state = saveName
        else:
            state = {saveName: saveIo}
        if includeMeta:
            state = self.addMetaProps(state, **metaFilterOpts)
        return state

    def __iter__(self):
        return iter([])


class NestedProcess(ProcessStage):
    def __init__(self, name: str = None):
        self.stages: t.List[ProcessStage] = []
        self.name = name
        self.allowDisable = True
        self.result = ProcessIO()

    def addFunction(self, func: t.Callable, **kwargs):
        """
        Wraps the provided function in an AtomicProcess and adds it to the current process.
        :param func: Forwarded to AtomicProcess
        :param kwargs: Forwarded to AtomicProcess
        """
        atomic = AtomicProcess(func, **kwargs)
        numSameNames = sum(atomic.name == stage.name.split("#")[0] for stage in self)
        if numSameNames > 0:
            atomic.name = f"{atomic.name}#{numSameNames+1}"
        if self.name is None:
            self.name = atomic.name
        self.stages.append(atomic)
        return atomic

    @classmethod
    def fromFunction(cls, func: t.Callable, **kwargs):
        name = kwargs.get("name", None)
        out = cls(name)
        out.addFunction(func, **kwargs)
        return out

    def addProcess(self, process: ProcessStage):
        if self.name is None:
            self.name = process.name
        self.stages.append(process)
        return process

    def updateInput(self, prevIo: ProcessIO = None, allowExtra=False, **kwargs):
        """Drill down to the necessary stages when setting input values when setter values are dicts"""
        if prevIo is None:
            prevIo = ProcessIO()
        prevIo.update(kwargs)
        # Make a copy to avoid in-place loss of keys
        prevIo = prevIo.copy()
        # List wrap instead of items() to avoid mutate error
        for kk in list(prevIo):
            vv = prevIo[kk]
            if isinstance(vv, dict):
                matchStage = [s for s in self if s.name == kk]
                if not matchStage:
                    # Since key doesn't match a stage name, assume it actually belongs to a parameter. This will be consumed below
                    continue
                else:
                    # TODO: Apply to first matching stage or all stages with this name?
                    matchStage[0].updateInput(**vv, allowExtra=allowExtra)
                    # Eliminate this key from global updates since it was locally consumed
                    prevIo.pop(kk)
        # Normal input maps to first stage, so propagate all normal args there
        # These are all args not matching a specific stage name. Dangerous to allow extra
        # in an unspecified stage, so turn it false otherwise all stages will grow many keys
        for stage in self.stages:
            stage.updateInput(prevIo, allowExtra=False)

    def run(self, io: ProcessIO = None, disable=False, **runKwargs):
        _activeIo = ProcessIO() if not io else _copy.copy(io)
        _activeIo.update(runKwargs)

        if self.disabled or disable and not self.result:
            # TODO: Formalize this behavior. Disabling before being run should avoid eating the input args
            return _activeIo

        for i, stage in enumerate(self):
            try:
                newIo = stage.run(_activeIo, disable=disable or self.disabled)
            except Exception as ex:
                # Provide information about which stage failed
                if not isinstance(ex.args, tuple):
                    ex.args = (ex.args,)
                ex.args = (stage,) + ex.args
                raise
            if isinstance(newIo, ProcessIO):
                _activeIo.update(newIo)

        self.result = _activeIo
        return self.result

    def saveState(self, includeDefaults=False, includeMeta=False, **metaFilterOpts):
        stageStates = []
        for stage in self:
            curState = stage.saveState(includeDefaults, includeMeta)
            stageStates.append(curState)
        saveName = self.nameForState or self.name
        state = {saveName: stageStates}
        if includeMeta:
            state = self.addMetaProps(state, **metaFilterOpts)
        return state

    def saveStateFlattened(self, **kwargs):
        """Saves state while collapsing all nested processes into one list of atomic processes"""
        return self.flatten().saveState(**kwargs)

    @property
    def input(self):
        return self.stages[0].input if self.stages else None

    def flatten(self, copy=True, includeDisabled=True):
        if copy:
            try:
                # No need to copy nested structure
                stages = self.stages
                self.stages = []
                outProc = _copy.copy(self)
            finally:
                self.stages = stages
        else:
            outProc = self
        outProc.stages = self._getFlatStages(includeDisabled)
        return outProc

    @property
    def stagesFlattened(self):
        """Property version of flattened self which, like `stages`, will always include disabled stages"""
        return self._getFlatStages()

    def _getFlatStages(self, includeDisabled=True):
        outStages: t.List[ProcessStage] = []
        for stage in self:
            if stage.disabled and not includeDisabled:
                continue
            if isinstance(stage, AtomicProcess):
                outStages.append(stage)
            else:
                stage: NestedProcess
                outStages.extend(stage._getFlatStages(includeDisabled))
        return outStages

    def __iter__(self):
        return iter(self.stages)

    def _stageSummaryWidget(self):
        raise NotImplementedError

    def _nonDisabledStagesFlattened(self):
        out = []
        for stage in self:
            if isinstance(stage, AtomicProcess):
                out.append(stage)
            elif not stage.disabled:
                stage: NestedProcess
                out.extend(stage._nonDisabledStagesFlattened())
        return out

    def stageSummaryGui(self, show=True):
        if self.result is None:
            raise RuntimeError(
                "Analytics can only be shown after the algorithm was run."
            )
        outGrid = self._stageSummaryWidget()
        if show:
            outGrid.showMaximized()

            def fixedShow():
                for item in outGrid.ci.items:
                    item.getViewBox().autoRange()

            QtCore.QTimer.singleShot(0, fixedShow)
        return outGrid

    def getAllStageInfos(self, ignoreDuplicates=True, ignoreDisabled=True):
        allInfos: _infoType = []
        lastInfos = []
        stages = (
            self._nonDisabledStagesFlattened()
            if ignoreDisabled
            else self.stagesFlattened
        )
        for stage in stages:
            infos = self.singleStageInfo(stage)
            if infos is None:
                continue
            if not ignoreDuplicates:
                validInfos = infos
            else:
                validInfos = self._cmpPrevCurInfos(lastInfos, infos)
            lastInfos = infos
            allInfos.extend(validInfos)
        return allInfos

    def singleStageInfo(self, stage: AtomicProcess):
        res = stage.result
        if not isinstance(res, ProcessIO) or any(k not in res for k in self.outMap):
            # Missing required keys, not sure how to turn into summary info. Skip
            return
        if "summaryInfo" not in res:
            defaultSummaryInfo = {k: res[k] for k in self.outMap}
            defaultSummaryInfo.update(name=stage.name)
            res["summaryInfo"] = defaultSummaryInfo
        if res["summaryInfo"] is None:
            return
        infos = stage.result["summaryInfo"]
        if not isinstance(infos, t.Sequence):
            infos = [infos]
        stageNameCount = 0
        for info in infos:
            if info.get("name", None) is None:
                newName = stage.name
                if stageNameCount > 0:
                    newName = f"{newName}#{stageNameCount}"
                info["name"] = newName
            stageNameCount += 1
        return infos

    @classmethod
    def _cmpPrevCurInfos(cls, prevInfos: t.List[dict], infos: t.List[dict]):
        """
        This comparison allows keys from the last result which exactly match keys from the
        current result to be discarded for brevity.
        """
        validInfos = []
        for info in infos:
            validInfo = _copy.copy(info)
            for lastInfo in prevInfos:
                for key in set(info.keys()).intersection(lastInfo.keys()) - {"name"}:
                    if np.array_equal(info[key], lastInfo[key]):
                        validInfo[key] = cls._DUPLICATE_INFO
            validInfos.append(validInfo)
        return validInfos
