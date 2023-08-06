from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Union

# -----
# DESCRIPTOR OVERLOADS
# -----

FilePath = Union[PathLike, str, Path]
