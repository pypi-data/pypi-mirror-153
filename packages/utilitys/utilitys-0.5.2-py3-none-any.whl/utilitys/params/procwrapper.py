from __future__ import annotations

from functools import singledispatch
from typing import Sequence, Callable

from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from .. import fns
from ..misc import CompositionMixin
from ..processing import *

__all__ = ["NestedProcWrapper", "addStageToParam"]


def _hookupCondition(parentParam: Parameter, chParam: Parameter):
    condition = chParam.opts.get("condition", None)
    if not condition:
        return
    _locals = {p.name(): p.value() for p in parentParam}
    if isinstance(condition, str):

        def cndtnCallable():
            exec(f"__out__ = bool({condition})", {}, _locals)
            # noinspection PyUnresolvedReferences
            return _locals["__out__"]

    else:
        cndtnCallable = condition

    def onChanged(param, val):
        _locals[param.name()] = val
        if cndtnCallable():
            chParam.show()
        else:
            chParam.hide()

    ch = None
    for ch in parentParam:
        ch.sigValueChanging.connect(onChanged)
    # Triger in case condition is initially false
    if ch:
        onChanged(ch, ch.value())


def _mkProcParam(stage: ProcessStage):
    return {
        "name": stage.name,
        "type": "procgroup",
        "process": stage,
        "enabled": not stage.disabled,
    }


@singledispatch
def addStageToParam(stage: ProcessStage, parentParam: Parameter, **kwargs):
    pass


@addStageToParam.register
def addAtomicToParam(
    stage: AtomicProcess,
    parentParam: Parameter,
    argNameFormat: Callable[[str], str] = None,
    nestHyperparams=True,
    **kwargs,
):
    descr = fns.docParser(stage.fnDoc).get("func-description", "")
    if nestHyperparams:
        parentParam = fns.getParamChild(parentParam, chOpts=_mkProcParam(stage))
    if descr:
        parentParam.setOpts(tip=descr)
    for key in stage.input.hyperParamKeys:
        pgParam = None
        if key in stage.input.params:
            pgParam = stage.input.params[key]
        if key in parentParam.names:
            # Child already exists, instead of adding this one, reassign the input
            stage.input.params[key] = parentParam.child(key)
        elif isinstance(pgParam, Parameter):
            if argNameFormat is not None:
                pgParam.setOpts(title=argNameFormat(key))
            parentParam.addChild(pgParam)
        if pgParam:
            _hookupCondition(parentParam, pgParam)
    return parentParam


@addStageToParam.register
def addNestedToParam(
    stage: NestedProcess,
    parentParam: Parameter,
    nestHyperparams=True,
    argNameFormat: Callable[[str], str] = None,
    treatAsAtomic=False,
    **kwargs,
):
    if nestHyperparams:
        parentParam = fns.getParamChild(parentParam, chOpts=_mkProcParam(stage))
    if treatAsAtomic:
        collapsed = AtomicProcess(stage.run, stage.name)
        collapsed.input = stage.input
        addAtomicToParam(collapsed, parentParam, argNameFormat)
        return
    for childStage in stage:
        addStageToParam(childStage, parentParam)
    return parentParam


class NestedProcWrapper(CompositionMixin):
    def __init__(
        self,
        processor: ProcessStage,
        parentParam: GroupParameter = None,
        argNameFormat: Callable[[str], str] = None,
        treatAsAtomic=False,
        nestHyperparams=True,
    ):
        self.processor = self.exposes(processor, "processor")
        self.algName = processor.name
        self.argNameFormat = argNameFormat
        self.treatAsAtomic = treatAsAtomic
        self.nestHyperparams = nestHyperparams
        # A few special things happen when adding a top-level processor. It has to create a parent if none exists without
        # doubly nesting and return a reference to the created parent param or the normal one if no nesting occurred.
        # The if-branching allows this to occur
        if parentParam is None:
            parentParam = Parameter.create(
                name=self.algName, type="procgroup", process=processor
            )
            # Avoid doubly-nested top parameter
            self.nestHyperparams = False
        self.parentParam: GroupParameter = parentParam

        self.addStage(self.processor)
        # Extract nested param if it was created
        if self.nestHyperparams:
            self.parentParam = parentParam.child(self.algName)

        # Reset once more if no initial parent param
        self.nestHyperparams = nestHyperparams

    def addStage(self, stage: ProcessStage, before: Sequence[str] = ()):
        parentParam = fns.getParamChild(self.parentParam, *before, allowCreate=False)
        parentStage: NestedProcess = self.getNestedName(self.processor, *before[:-1])
        # Defensive check to only add extra stages onto existing processor
        if stage is not self.processor:
            if before:
                tmpStage = self.getNestedName(parentStage, before[-1])
                beforeIdx = parentStage.stages.index(tmpStage)
                parentStage.stages = (
                    parentStage.stages[:beforeIdx]
                    + [stage]
                    + parentStage.stages[beforeIdx:]
                )
            else:
                parentStage.stages.append(stage)
        addStageToParam(
            stage,
            parentParam,
            argNameFormat=self.argNameFormat,
            treatAsAtomic=self.treatAsAtomic,
            nestHyperparams=self.nestHyperparams,
        )

    def removeStage(self, *nestedName: str):
        parent = self.getNestedName(self.processor, *nestedName[:-1])
        stage = self.getNestedName(parent, nestedName[-1])
        parent.stages.remove(stage)
        parentParam = fns.getParamChild(
            self.parentParam, *nestedName[:-1], allowCreate=False
        )
        childParam = fns.getParamChild(parentParam, nestedName[-1], allowCreate=False)
        parentParam.removeChild(childParam)

    def clear(self):
        if isinstance(self.processor, AtomicProcess):
            raise AttributeError("Cannot clear a wrapper of an atomic process")
        self.processor: NestedProcess
        for stage in self.processor.stages:
            self.removeStage(stage.name)

    def setStageEnabled(self, stageIdx: Sequence[str], enabled: bool):
        paramForStage = self.parentParam.child(*stageIdx)
        prevEnabled = paramForStage.opts["enabled"]
        if prevEnabled != enabled:
            paramForStage.setOpts(enabled=enabled)

    def __repr__(self) -> str:
        selfCls = type(self)
        oldName: str = super().__repr__()
        # Remove module name for brevity
        oldName = oldName.replace(
            f"{selfCls.__module__}.{selfCls.__name__}",
            f"{selfCls.__name__} '{self.algName}'",
        )
        return oldName

    @classmethod
    def getNestedName(cls, curProc: ProcessStage, *nestedName: str):
        if not nestedName or isinstance(curProc, AtomicProcess):
            return curProc
        # noinspection PyUnresolvedReferences
        for stage in curProc:
            if stage.name == nestedName[0]:
                if len(nestedName) == 1:
                    return stage
                else:
                    return cls.getNestedName(stage, *nestedName[1:])
        # Requested stage not found if execution reaches here
        raise ValueError(f"Stage {nestedName} not found in {curProc}")
