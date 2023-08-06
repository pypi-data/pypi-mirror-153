"""
Further subtyping of `GenericSurface` to be either an `IrregularSurface`
or `RegularSurface` depending on mesh connectivity.
"""

from dataclasses import dataclass
from os import PathLike
from typing import TypeVar, Generic, Sequence, Optional

from civet.abstract_data import AbstractDataCommand
from civet.bases import DataSource
from civet.extraction.side import Side
from civet.obj import GenericSurface

_IS = TypeVar('_IS', bound='GenericIrregularSurface')
_RS = TypeVar('_RS', bound='GenericRegularSurface')


@dataclass(frozen=True)
class Tetra(DataSource):

    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    radius: tuple[float, float, float] = (1.0, 1.0, 1.0)
    triangles: int = 81920

    def command(self, output: str | PathLike) -> Sequence[str | PathLike]:
        return 'create_tetra', output, *self.center, *self.radius


class RegularSurface(GenericSurface[_RS], Generic[_RS]):
    """
    Represents a mesh (`.obj`) with standard connectivity.

    Typically, standard connectivity means 81,920 triangles, 41,962
    vertices. By convention, the file name for such a surface should
    have the suffix `_81920.obj`.

    A general definition for "standard connectivity" would be a
    polygonal mesh of *N* triangles where 320 and 4 are common
    denominators of *N*.
    """
    @classmethod
    def create_tetra(cls, tetra: Tetra) -> 'RegularSurface[RegularSurface]':
        return cls(tetra)


class IrregularSurface(GenericSurface[_IS], Generic[_IS]):
    """
    Represents a mesh (`.obj`) with irregular connectivity.
    """
    def interpolate_with_sphere(
            self,
            side: Optional[Side] = None,
            n_inflate: Optional[int] = None,
            n_smooth: Optional[int] = None
    ) -> RegularSurface:
        """
        Resample this surface to have a standard number of 81,920 triangles.

        If `n_inflate` and `n_smooth` are given, use `inflate_to_sphere_implicit` instead
        of `inflate_to_sphere`.
        """
        options = []
        if side is not None:
            options += ['-' + side.value]
        if (n_inflate is None) ^ (n_smooth is None):
            raise ValueError('both n_inflate and n_smooth must be specified')
        if n_inflate is not None and n_smooth is not None:
            options += ['-inflate', str(n_inflate), str(n_smooth)]

        class InterpolatedFromSphere(RegularSurface):
            def command(self, output: str | PathLike
                        ) -> Sequence[str | PathLike | AbstractDataCommand]:
                return 'interpolate_surface_with_sphere.pl', *options, self.input, output
        return InterpolatedFromSphere(self)
