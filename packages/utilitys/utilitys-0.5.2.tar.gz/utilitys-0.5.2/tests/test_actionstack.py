import numpy as np
import pytest

from utilitys.misc import ActionStack, DeferredActionStackMixin as DASM

COUNT = 10


class StackForTesting(ActionStack):
    def __init__(self):
        super().__init__()

        @self.undoable()
        def op(num=None):
            if num is None:
                num = len(self.lst)
            self.lst.append(num)
            yield
            self.lst.pop()

        @self.undoable("recurse")
        def recursiveOp_swapEveryTwo(lst=None):
            if lst is None:
                lst = self.lst
            sz = len(lst)
            if sz < 2:
                pass
            elif sz < 4:
                tmp = lst[0]
                lst[0] = lst[1]
                lst[1] = tmp
            else:
                for rng in slice(sz // 2), slice(sz // 2, sz):
                    lst[rng] = recursiveOp_swapEveryTwo(lst[rng])
            yield lst
            recursiveOp_swapEveryTwo(lst)

        def grpOp():
            with self.group("grouping"):
                for _ in range(COUNT):
                    self.op()

        self.recursive = recursiveOp_swapEveryTwo
        self.grpOp = grpOp
        self.op = op

        self.lst = []

    def clear(self):
        super().clear()
        self.lst.clear()


def test_group():
    stack = StackForTesting()
    stack.grpOp()
    stack.op()
    assert stack.lst == list(range(COUNT + 1))
    stack.undo()
    assert stack.lst == list(range(COUNT))
    stack.undo()
    assert stack.lst == []


def test_nested_doable():
    stack = StackForTesting()

    @stack.undoable("outer op")
    def outer():
        stack.lst.append(str(len(stack.lst)))
        stack.op()
        yield
        stack.lst.pop()
        stack.lst.pop()

    outer()
    assert stack.lst == ["0", 1]
    stack.undo()
    assert stack.lst == []


def test_recursive():
    stack = StackForTesting()

    nextPow2 = int(np.power(2, np.ceil(np.log2(COUNT))))
    stack.lst = list(range(nextPow2))
    origLst = stack.lst.copy()

    stack.recursive()
    swapped = stack.lst.copy()

    stack.undo()
    assert stack.lst == origLst

    stack.redo()
    assert stack.lst == swapped
    assert len(stack.actions) == 1


def test_bad_undo():
    stack = StackForTesting()

    for _ii in range(4):
        stack.op()
    for _ii in range(4):
        stack.undo()
    with pytest.warns(UserWarning):
        stack.undo()


def test_bad_redo():
    stack = StackForTesting()
    with pytest.warns(UserWarning):
        stack.redo()
    stack.op()
    with pytest.warns(UserWarning):
        stack.undo()
        stack.redo()
        stack.redo()


def test_invalidate_redos():
    stack = StackForTesting()

    for ii in range(COUNT):
        stack.op()

    assert stack.lst == list(range(COUNT))
    numEntriesToRemomve = COUNT // 3
    for ii in range(numEntriesToRemomve):
        stack.undo()

    numRemainingEntries = COUNT - numEntriesToRemomve
    assert np.sum([a.treatAsUndo for a in stack.actions]) == numRemainingEntries

    stack.op(1)
    # New action should flush old ones
    with pytest.warns(UserWarning):
        stack.redo()
    stack.undo()
    assert len(stack.actions) == numRemainingEntries + 1
    cmplst = list(range(numRemainingEntries))
    assert stack.lst == cmplst
    stack.redo()
    assert stack.lst == cmplst + [1]


def test_ignore_acts():
    stack = StackForTesting()
    with stack.ignoreActions():
        for _ in range(COUNT):
            stack.op()
    assert len(stack.actions) == 0
    with pytest.warns(UserWarning):
        stack.undo()


def test_max_len():
    stack = StackForTesting()
    cnt = stack.actions.maxlen + 20
    for ii in range(cnt):
        stack.op()

    with pytest.warns(UserWarning):
        for ii in range(cnt):
            stack.undo()


def test_grp_composite():
    stack = StackForTesting()
    with stack.group("outer grp", flushUnusedRedos=True):
        with stack.group("inner grp"):
            stack.grpOp()
            stack.recursive()
        stack.op()
        stack.grpOp()
        stack.op()
    assert len(stack.actions) == 1

    postOpLst = stack.lst.copy()
    stack.undo()
    assert len(stack.lst) == 0
    stack.redo()
    assert postOpLst == stack.lst


def test_savepoint():
    stack = StackForTesting()

    for _ in range(COUNT):
        stack.op()
    stack.setSavepoint()

    stack.op()
    assert stack.changedSinceLastSave

    stack.revertToSavepoint()
    assert not stack.changedSinceLastSave

    stack.op()
    stack.op()

    stack.revertToSavepoint()
    assert stack.lst == list(range(COUNT))


def test_reassign_backward():
    stack = StackForTesting()
    newlst = []
    newAppend = lambda: newlst.append(5)
    # Test in forward state
    for _ in range(COUNT):
        stack.op()
        stack.actions[-1].reassignBackward(newAppend)
    for _ in range(COUNT):
        stack.undo()
    assert len(stack.actions) == COUNT
    assert newlst == [5] * COUNT

    # Make sure it works going backward
    for _ in range(COUNT):
        stack.redo()
    assert len(stack.lst) == 2 * COUNT
    for _ in range(COUNT):
        stack.undo()
    assert newlst == [5] * COUNT * 2

    # Make sure doing reassign after undo works too
    stack.clear()
    newlst.clear()
    for _ in range(COUNT):
        stack.op()
    for _ in range(COUNT):
        stack.undo()
    for ii in range(COUNT):
        stack.actions[ii].reassignBackward(newAppend)
    for _ in range(COUNT):
        stack.redo()
    for _ in range(COUNT):
        stack.undo()
    assert newlst == [5] * COUNT


def test_deferred_stack():
    class A(DASM):
        @DASM.undoable("test")
        def test(self, num: int):
            print(num)
            yield
            print(num + 1)

        @DASM.undoable("test 2")
        def moretest(self, x=1, y=3):
            print(dict(x=x, y=y))
            yield
            print(dict(x=x + 1, y=y + 1))

    class B(A):
        pass

    class C(A):
        @B.undoable("this one")
        def test2(self):
            yield "test 2 first"
            return "test 2 second"

    class D(C):
        pass

    a = A()
    with A.setStack(ActionStack()):
        b = B()
        c = C()
    assert a.actionStack is not b.actionStack
    assert b.actionStack is c.actionStack

    with B.setStack(ActionStack()):
        a = A()
        b = B()
        c = C()
        d = D()
    # B.setstack means a (as an earlier class in the hierarchy) should not be set
    # Also, C (and D) didn't come from B, so those shouldn't be overridden either
    assert a.actionStack is not b.actionStack is not c.actionStack is not d.actionStack

    with C.setStack(ActionStack()):
        a = A()
        b = B()
        c = C()
        d = D()
    assert a.actionStack is not b.actionStack is not c.actionStack is d.actionStack

    C.actionStack = mystack = ActionStack()
    d = D()
    assert d.actionStack is mystack
    with C.setStack(ActionStack()):
        c = C()
    # Make sure reset happens correctly
    assert C.actionStack is mystack
    assert c.actionStack is not mystack
