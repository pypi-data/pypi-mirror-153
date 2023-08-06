"""
Submodule for more specific types which are relevant to
surface-extraction subroutines of the CIVET pipeline.
"""

from civet.extraction.side import Side
from civet.extraction.hemisphere import HemisphereMask
from civet.extraction.surfaces import RegularSurface, IrregularSurface, Tetra
from civet.extraction.starting_models import SurfaceModel

__all__ = [
    'HemisphereMask',
    'Side',
    'RegularSurface',
    'IrregularSurface',
    'Tetra',
    'SurfaceModel'
]
