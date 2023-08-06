"""
All API discrepancies between different systems, python versions, etc. should be resolved here if remotely possible
"""
import sys

__all__ = ["typing_extensions"]

if sys.version_info < (3, 8):
    import typing_extensions
else:
    import typing as typing_extensions
