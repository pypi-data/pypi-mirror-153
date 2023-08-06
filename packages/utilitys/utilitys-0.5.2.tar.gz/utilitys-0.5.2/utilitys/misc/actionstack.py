"""
Inspired by 'undo' on pypi (https://bitbucket.org/aquavitae/undo/src/default/)
but there are many flaws and the project is not under active development. It is
also less pythonic than it could be, using functions where properties are more
appropriate.
"""
from __future__ import annotations
import contextlib
import copy
import typing as t
from contextlib import contextmanager
from warnings import warn
from collections import deque
from functools import wraps

from utilitys.fns import gracefulNext

__all__ = ["ActionStack", "Action", "DeferredActionStackMixin"]

# _generatorCallable = Callable[[...], Union[Generator, Any]]
class Action:
    """
    This represents an action which can be done and undone.
    """

    def __init__(
        self,
        generator: t.Callable[..., t.Union[t.Generator, t.Any]],
        args: tuple = None,
        kwargs: dict = None,
        descr: str = None,
        treatAsUndo=False,
    ):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if descr is None:
            descr = generator.__name__
        self._generator = generator
        self.args = args
        self.kwargs = kwargs
        self.descr = descr
        self._runner = None

        self.treatAsUndo = treatAsUndo
        if treatAsUndo:
            # Need to init runner for when backward is called
            self._runner = self._generator(*args, **kwargs)

    def reassignBackward(
        self, backwardFn: t.Callable[..., t.Any], backwardArgs=(), backwardKwargs=None
    ):

        if backwardKwargs is None:
            backwardKwargs = {}
        oldGenerator = self._generator

        def newGenerator(*args, **kwargs):
            # Keep forward
            yield next(oldGenerator(*args, **kwargs))
            # Alter backwards
            yield backwardFn(*backwardArgs, **backwardKwargs)

        self._generator = newGenerator
        if self.treatAsUndo:
            # Already in current runner, so change it
            def newRunner():
                yield backwardFn(*backwardArgs, **backwardKwargs)

            self._runner = newRunner()

    def forward(self, graceful=False):
        """
        Do or redo the action

        :param graceful: Whether to show an error on stop iteration or not. If a function
          is registered as undoable but doesn't contain a yield expression this is useful,
          i.e. performing a redo when that redo may not have a corresponding undo again
        """
        self._runner = self._generator(*self.args, **self.kwargs)
        if not graceful:
            ret = next(self._runner)
        else:
            ret = gracefulNext(self._runner)
        # Forward use is expired, so treat as backward now
        self.treatAsUndo = True
        return ret

    def backward(self):
        """Undo the action"""
        # It's OK if this raises StopIteration, since we don't need anything after
        # calling it. Therefore call graceful next.
        ret = gracefulNext(self._runner)
        # Delete it so that its not accidentally called again
        del self._runner
        self.treatAsUndo = False
        return ret

    def __repr__(self):
        selfCls = type(self)
        oldName: str = super().__repr__()
        # Remove module name for brevity
        oldName = oldName.replace(
            f"{selfCls.__module__}.{selfCls.__name__}",
            f"{selfCls.__name__} '{self.descr}'",
        )
        return oldName


class EMPTY:
    pass


EmptyType = t.Type[EMPTY]


class LIB_LOCK:
    pass


class USER_LOCK:
    pass


class ActionStack:
    """The main undo stack.

    The two key features are the :func:`redo` and :func:`undo` methods. If an
    exception occurs during doing or undoing a undoable, the undoable
    aborts and the stack is cleared to avoid any further data corruption.

    The stack provides two properties for tracking actions: *docallback*
    and *undocallback*. Each of these allow a callback function to be set
    which is called when an action is done or undone repectively. By default,
    they do nothing.
    """

    def __init__(self, maxlen: int = 50):
        self.actions: t.Deque[Action] = deque(maxlen=maxlen)
        self.currentActionBuffer = self.actions
        self._savepoint: t.Union[EmptyType, Action] = EMPTY
        self.stackChangedCallbacks: t.List[t.Callable] = []
        self._locks = []

    @contextlib.contextmanager
    def group(self, descr: str = None, flushUnusedRedos=False):
        """Return a context manager for grouping undoable actions.

        All actions which occur within the group will be undone by a single call
        of `stack.undo`.
        """
        newActBuffer: t.Deque[Action] = deque()
        with _BufferOverride(self, newActBuffer):
            yield

        def grpAct():
            for _ in range(2):
                for act in newActBuffer:
                    if act.treatAsUndo:
                        act.backward()
                    else:
                        act.forward(graceful=True)
                yield

        if not self.locked:
            self.currentActionBuffer.append(
                Action(grpAct, descr=descr, treatAsUndo=True)
            )
        if flushUnusedRedos:
            self.flushUnusedRedos()

    def undoable(self, descr=None, asGroup=False, copyArgs=False):
        """Decorator which creates a new undoable action type.

        Parameters
        ___________
        :param descr: Description of this action, e.g. "add components", etc.
        :param asGroup: If *True* assumes this undoable function is a composition
          of other undoable functions. This is a simple alias for
          >>> stack: ActionStack, func: t.Callable, args: tuple, kwargs: dict
          >>> with stack.group('descr', flushUnusedRedos=True):
          >>>  func(*args, **kwargs)
        :param copyArgs: Whether to make a copy of the arguments used for the undo
          function. This is useful for functions where the input argument is modified
          during the function call. WARNING: UNTESTED
        """

        def decorator(generatorFn: t.Callable[..., t.Generator]):
            nonlocal descr
            if descr is None:
                descr = generatorFn.__name__

            @wraps(generatorFn)
            def inner_group(*args, **kwargs):
                with self.group(descr, flushUnusedRedos=True):
                    ret = generatorFn(*args, **kwargs)
                self.processCallbacks(self.actions[-1])
                return ret

            @wraps(generatorFn)
            def inner_action(*args, **kwargs):
                shouldAppend = True
                if copyArgs:
                    args = tuple(copy.copy(arg) for arg in args)
                    kwargs = {k: copy.copy(v) for k, v in kwargs.items()}
                action = Action(generatorFn, args, kwargs, descr)
                try:
                    with self.ignoreActions(LIB_LOCK):
                        ret = action.forward()
                except StopIteration as ex:
                    ret = ex.value
                    shouldAppend = False
                if not self.locked and shouldAppend:
                    self.currentActionBuffer.append(action)
                    # State change of application means old redos are invalid
                    self.flushUnusedRedos()
                # Else: doesn't get added to the queue
                # Possible this action never added a generator entry (i.e. "return"ed instead of "yield"ing)
                # Prevent this entry from looking like it went to the stack by using "None"
                if not shouldAppend:
                    action = None
                self.processCallbacks(action)
                return ret

            if asGroup:
                return inner_group
            else:
                return inner_action

        return decorator

    def processCallbacks(self, lastAction=None):
        if self.currentActionBuffer is self.actions:
            for callback in self.stackChangedCallbacks:
                callback(lastAction)

    @property
    def undoDescr(self):
        if self.canUndo:
            return self.actions[-1].descr
        else:
            return None

    @property
    def redoDescr(self):
        if self.canRedo:
            return self.actions[0].descr
        else:
            return None

    @property
    def canUndo(self):
        """Return *True* if undos are available"""
        return len(self.actions) > 0 and self.actions[-1].treatAsUndo

    @property
    def canRedo(self):
        """Return *True* if redos are available"""
        return len(self.actions) > 0 and not self.actions[0].treatAsUndo

    def resizeStack(self, maxLength: int):
        """
        Updates buffer size to the new specification. If the new size is smaller,
        only the most recent actions are kept.
        :param maxLength:
        """
        if maxLength == self.actions.maxlen:
            return
        newDeque: t.Deque[Action] = deque(maxlen=maxLength)
        newDeque.extend(self.actions)
        receiverNeedsReset = True if not self.locked else False
        self.actions = newDeque
        if receiverNeedsReset:
            self.currentActionBuffer = self.actions

    def flushUnusedRedos(self):
        flushed = False
        while self.canRedo:
            if self.actions[0] is self._savepoint:
                self._savepoint = EMPTY
            self.actions.popleft()
            flushed = True
        if flushed:
            self.processCallbacks()

    def revertToSavepoint(self):
        if self._savepoint is EMPTY:
            raise ValueError(
                "Attempted to revert to empty savepoint. Perhaps you"
                " performed several 'undo' operations, then performed"
                " a forward operation that flushed your savepoint?"
            )
        if self._savepoint.treatAsUndo:
            actFn = self.undo
        else:
            actFn = self.redo
        reverted = False
        while self.changedSinceLastSave:
            actFn()
            reverted = True
        if reverted:
            self.processCallbacks()

    def redo(self):
        """
        Redo the last undone action.

        This is only possible if no other actions have occurred since the
        last undo call.
        """
        if not self.canRedo:
            warn("Nothing to redo", UserWarning, stacklevel=2)
            return

        self.actions.rotate(-1)
        with self.ignoreActions(LIB_LOCK):
            ret = self.actions[-1].forward(graceful=True)
        self.processCallbacks(self.actions[-1])
        return ret

    def undo(self):
        """
        Undo the last action.
        """
        if not self.canUndo:
            warn("Nothing to undo", UserWarning, stacklevel=2)
            return

        with self.ignoreActions(LIB_LOCK):
            ret = self.actions[-1].backward()
        self.actions.rotate(1)
        # After rotation, action is now at spot 0
        self.processCallbacks(self.actions[0])
        return ret

    def clear(self):
        """Clear the undo list."""
        self._savepoint = EMPTY
        self.actions.clear()
        self.processCallbacks()

    def setSavepoint(self):
        """Set the savepoint."""
        if self.canUndo:
            self._savepoint = self.actions[-1]
        else:
            self._savepoint = EMPTY

    @property
    def changedSinceLastSave(self):
        """Return *True* if the state has changed since the savepoint.

        This will always return *True* if the savepoint has not been set.
        """
        if self._savepoint is EMPTY:
            return False
        elif self._savepoint.treatAsUndo:
            cmpAction = self.actions[-1]
        else:
            cmpAction = self.actions[0]
        return self._savepoint is not cmpAction

    @property
    def lockedByUser(self):
        return any(l != LIB_LOCK for l in self._locks)

    @property
    def locked(self):
        return len(self._locks) > 0

    def ignoreActions(self, lock=USER_LOCK):
        return BufferLock(self, lock)


class _BufferOverride:
    def __init__(self, stack: ActionStack, newActQueue: deque = None):
        self.newActQueue = newActQueue
        self.stack = stack

        self.oldStackActions = None

    def __enter__(self):
        stack = self.stack
        # Deisgned for internal use, so OK to use protected member
        # noinspection PyProtectedMember
        self.oldStackActions = stack.currentActionBuffer
        stack.currentActionBuffer = self.newActQueue
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stack.currentActionBuffer = self.oldStackActions


class BufferLock:
    def __init__(self, stack, lock=USER_LOCK):
        self.lock = lock
        self.stack = stack

    def __enter__(self):
        self.stack._locks.append(self.lock)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stack._locks.remove(self.lock)


class DeferredActionStackMixin:
    """
    When registering undoable actions of a class with an action stack, it is impossible to use the reference stack's
    decorator since the stack isn't constructed yet. Moreover, creating a class-level default stack and registering all
    actions to it will force all instances of that class to share the same undo buffer. this deferred undoable solves the
    problem. It will record which functions the user wants to register as undoable, and the initialization procedure of
    ActionStackMixin will complete this registration as instances are created. That way, instances of the same class
    have the option of sharing undo buffers, but aren't forced to do so.

    This has the same effect as registering undoable actions in the __init__ body, e.g.:

    ```python
      def __init__(self, ...):
        self.func1 = self.actionStack.undoable('descr')(func1)

        self.func2 = self.actionStack.undoable()(func2)

        # ...
    ```

    Note that deferred action stacks colocate generator functions with their "undoable" registration to avoid confusion,
    promote reuse, etc.
    """

    actionStack: ActionStack = None
    _deferredUndoables = {}

    class undoable:
        """
        Intended for use solely as a function decorator where ActionStack.undoable would be used. It's deferred nature,
        though, means no stack object must exist at the time of registering the undoable function. Instead, a stack is
        provided for this function on creationg of the ActionStackMixin class.
        """

        def __set_name__(self, owner: t.Type[DeferredActionStackMixin], name):
            if not issubclass(owner, DeferredActionStackMixin):
                raise TypeError(
                    "Can only use deferred undoable on ActionStackMixin classes"
                )
            # At this point, we at some point had acecss to the decorated function, deco description/args, and finally
            # we have the owning class. Add a deferred undoable to be later registered. This is a bit tricky, since a plain
            # reference to _deferredUndoables may share references to other classes (which we don't want). Using copy()
            # ensures the default stack is unique to *this* class, preventing one class from registering methods of another.
            defUndos = owner._deferredUndoables.copy()
            defUndos[name] = self.regArgs
            owner._deferredUndoables = defUndos

        def __init__(self, *args, **kwargs):
            self.regArgs = (args, kwargs)
            super().__init__()

        def __get__(self, instance, owner):
            return self.func.__get__(instance, owner)

        def __call__(self, func):
            self.func = func
            return self

    def __new__(cls, *args, **kwargs):
        stack = cls.actionStack if cls.actionStack else ActionStack()
        obj = super().__new__(cls, *args, **kwargs)
        obj.actionStack = stack
        for funcName, (regArgs, regKwargs) in cls._deferredUndoables.items():
            bound = getattr(obj, funcName)
            registered = stack.undoable(*regArgs, **regKwargs)(bound)
            setattr(obj, funcName, registered)
        return obj

    @classmethod
    @contextmanager
    def setStack(cls, stack: ActionStack):
        """
        Allows the code instantiating deferred stack objects to set the desired undo stack for that new instance. This is
        reverted back the the original value upon exiting the context manager
        :param stack: Stack to which undo actions should be registered
        :return: Context manager that resets the default registration stack on exit
        """
        oldStack = cls.actionStack
        cls.actionStack = stack
        yield
        cls.actionStack = oldStack
