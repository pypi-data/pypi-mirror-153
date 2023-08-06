from __future__ import annotations

from typing import Optional, Collection, Sequence

import numpy as np
import pandas as pd


def _rescale(data, min_, max_):
    # Handle nan values
    rng = max_ - min_
    if rng == 0:
        return np.ones_like(data)
    return (data.astype(float) - min_) / rng


class _UNSPECIFIED_DEFAULT:
    pass


class PrjParam:
    comparator = str
    """Function for determining =/</> when comparing to another object"""

    def __init__(
        self, name: str, value=None, pType: Optional[str] = None, helpText="", **opts
    ):
        """
        Encapsulates parameter information use within the main application

        :param name: Display name of the parameter
        :param value: Initial value of the parameter. This is used within the program
          to infer parameter type, shape, comparison methods, etc.
        :param pType: Type of the variable if not easily inferrable from the value itself.
          For instance, class:`FRShortcutParameter<s3a.views.parameditors.FRShortcutParameter>`
          is indicated with string values (e.g. 'Ctrl+D'), so the user must explicitly specify
          that such an :class:`PrjParam` is of type 'shortcut' (as defined in
          :class:`FRShortcutParameter<s3a.views.parameditors.FRShortcutParameter>`)
          If the type *is* easily inferrable, this may be left blank.
        :param helpText: Additional documentation for this parameter.
        :param opts: Additional options associated with this parameter
        """
        if opts is None:
            opts = {}
        if pType is None:
            # Infer from value
            pType = type(value).__name__.lower()
        self.name = name
        self.value = value
        self.pType = pType
        self.helpText = helpText or opts.get("tip", "")

        self.opts = opts

        self.group: Optional[Collection[PrjParam]] = None
        """
    PrjParamGroup to which this parameter belongs, if this parameter is part of
      a group. This is set by the PrjParamGroup, not manually
    """

    def toPgDict(self):
        """
        Simple conversion function from PrjParams used internally to the dictionary form expected
        by pyqtgraph parameters
        """
        opts = self.opts.copy()
        opts.pop("type", "name")
        paramOpts = dict(name=self.name, type=self.pType, **opts)
        if len(self.helpText) > 0 and not paramOpts.get("tip", None):
            paramOpts["tip"] = self.helpText
        if self.pType == "group" and self.value is not None:
            paramOpts.update(children=self.value)
        else:
            paramOpts.update(value=self.value)
        return paramOpts

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}: <{self.pType}>"

    def __lt__(self, other):
        """
        Required for sorting by value in component table. Defer to alphabetic
        sorting
        :param other: Other :class:`PrjParam` member for comparison
        :return: Whether `self` is less than `other`
        """
        return self.comparator(self) < self.comparator(other)

    def __eq__(self, other):
        # TODO: Highly naive implementation. Be sure to make this more robust if it needs to be
        #   for now assume only other prjparamss will be passed in
        return self.comparator(self) == self.comparator(other)

    def __hash__(self):
        # Since every param within a group will have a unique name, just the name is
        # sufficient to form a proper hash
        return hash(
            self.comparator(self),
        )

    def toNumeric(self, data: Sequence, rescale=False, returnMapping=False):
        """
        Useful for converting string-like or list-like parameters to integer representations.
        If self's `value` is non-numeric data (e.g. strings):
           - First, the parameter is searched for a 'limits' property. This will contain all
             possible values this field could be.
           - If no limits exist, unique values in the input data will be considered the
             limits
        :param data: Array-like data to be turned into numeric values according to the parameter type
        :param rescale: If *True*, values will be rescaled to the range 0-1
        :param returnMapping: Whether to also return an array of the unique values within `data`.
          If data is already numeric, *None* is returned instead of this array.
        """
        numericVals = np.asarray(data).copy()
        if len(data) == 0:
            mapping = pd.Series(name=self, dtype=object)
            if returnMapping:
                return numericVals, mapping
            return numericVals
        if not np.issubdtype(type(self.value), np.number):
            # Check for limits that indicate the exhaustive list of possible values.
            # Otherwise, just use the unique values of this set as the limits
            if "limits" in self.opts:
                listLims = list(self.opts["limits"])
                numericVals = np.array([listLims.index(v) for v in numericVals])
                mapping = pd.Series(listLims, np.arange(len(listLims), dtype=int))
            else:
                listLims, numericIdxs, numericVals = np.unique(
                    numericVals, return_index=True, return_inverse=True
                )
                mapping = pd.Series(listLims, numericVals[numericIdxs], name=self)
        elif returnMapping:
            # Potentially expensive, only compute if requested
            uniques = np.unique(numericVals)
            mapping = pd.Series(uniques, uniques, name=self)
        else:
            # Dummy mapping to allow ops
            class mapping:
                index = np.array([numericVals.max(), numericVals.min()])

        if rescale:
            min_, max_ = mapping.index.min(), mapping.index.max()
            # Make sure to reduce min to account for offset in reverse direction
            numericVals = _rescale(numericVals, min_, max_)
            mapping.index = _rescale(mapping.index, min_, max_)
        if returnMapping:
            return numericVals, mapping
        return numericVals

    def __getitem__(self, item):
        if item in self._fields:
            return getattr(self, item)
        return self.opts[item]

    def __setitem__(self, key, value):
        if key in self._fields:
            setattr(self, key, value)
        else:
            self.opts[key] = value

    def get(self, item, default=_UNSPECIFIED_DEFAULT):
        try:
            return self[item]
        except KeyError:
            if default is _UNSPECIFIED_DEFAULT:
                raise
            return default

    @property
    def _fields(self):
        excludeFields = {"group", "opts"}
        return [field for field in self.__dict__ if field not in excludeFields]

    def keys(self):
        return self._fields + list(self.opts.keys())

    def __contains__(self, item):
        return item in self._fields or item in self.opts

    def addHelpText(self, prependText="", postfixText="", replace=True, newline="<br>"):
        helpText = self.helpText
        if len(prependText) > 0 and len(helpText) > 0 or len(postfixText) > 0:
            prependText += newline
        curText = prependText + self.helpText
        if len(postfixText) > 0:
            curText += newline + postfixText
        if replace:
            self.helpText = curText
        return curText
