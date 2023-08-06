import typing as t
import weakref


class _NAME_STR(str):
    """Helper class just used to distinguish between an object reference to a string and a string name of a dict key"""

    pass


T = t.TypeVar("T")


class CompositionMixin:
    """
    Python has great built-in support for subclassing. However, another common use case is composition-based inheritence,
    which involves a has-a relationship rather than an is-a relationship. Curently, this involves for-looping over the
    attributes from a compositional object to assign them to self, and even this may fail if these attributes aren't
    callable, i.e. if the reference can go stale. This is a helper mixin which allows compositional code to be easily
    written without for-looping over attributes or providing stale references.
    """

    _exposedObjs = []

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._exposedObjs = []
        obj._allowRecurse = True
        return obj

    def exposes(self, obj: T, name: str = None) -> T:
        """
        Adds `obj` attributes/methods to `self` mro / lookup list for easily making `obj` transparent to consumers of `self`
        :param obj: Object to expose
        :param name: Often, object references can be reassigned. In theses cases, providing a name as well will trigger a
          lookup of this object from self when needed rather than relying on the object reference directly
        """
        # Keep only the name in case reference object is altered
        name = obj if name is None else _NAME_STR(name)
        self._exposedObjs.append(name)
        return obj

    def __getattr__(self, item):
        if not self._allowRecurse:
            # Already came here from a previous call where no attribute was found
            raise AttributeError(item)
        self._allowRecurse = False
        for objOrName in self._exposedObjs:
            if isinstance(objOrName, _NAME_STR):
                objOrName = getattr(self, objOrName)
            if hasattr(objOrName, item):
                self._allowRecurse = True
                return getattr(objOrName, item)
        try:
            # Handled by try-except
            # noinspection PyUnresolvedReferences
            ret = super().__getattr__(item)
        except AttributeError:
            raise AttributeError(item)
        finally:
            self._allowRecurse = True
        return ret
