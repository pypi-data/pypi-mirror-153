"""
Types related to xfm transformations
(`param2xfm`, `transform_objects`, `transform_volume`).
"""
import abc
from os import PathLike
from typing import Sequence, TypeVar, Literal
from civet.abstract_data import AbstractDataCommand
from civet.bases import DataSource, DataFile
from enum import Enum
from dataclasses import dataclass


class Transformations(Enum):
    CENTER = '-center'
    TRANSLATION = '-translation'
    ROTATIONS = '-rotations'
    SCALES = '-scales'
    SHEARS = '-shears'


@dataclass(frozen=True)
class Xfm(DataSource):
    """
    Represents a `.xfm` file created by `param2xfm`.

    `Xfm` can only represent a single `param2xfm` option.
    Would be nice to support multiple transformations in go, but it's not implemented.
    """

    transformation: Transformations
    x: float
    y: float
    z: float
    preferred_suffix = '.xfm'

    def command(self, output: str | PathLike) -> Sequence[str | PathLike | AbstractDataCommand]:
        return 'param2xfm', self.transformation.value, str(self.x), str(self.y), str(self.z), output


TransformProgram = Literal['transform_objects', 'transform_volume']
_T = TypeVar('_T', bound='TransformableMixin')


@dataclass(frozen=True)
class TransformableMixin(DataFile[_T], abc.ABC):
    @property
    @abc.abstractmethod
    def transform_program(self) -> TransformProgram:
        """
        Specifies which program is used to transform objects of this type.
        """
        ...

    def append_xfm(self, xfm: Xfm) -> _T:
        def command(output: str | PathLike) -> Sequence[str | PathLike | AbstractDataCommand]:
            return self.transform_program, self, xfm, output
        return self.create_command(command)

    def flip_x(self) -> _T:
        """
        Flip this surface along the *x*-axis.
        """
        return self.append_xfm(Xfm(Transformations.SCALES, -1, 1, 1))

    def translate_x(self, x: float) -> _T:
        """
        Translate this surface along the *x*-axis.
        """
        return self.append_xfm(Xfm(Transformations.TRANSLATION, x, 0, 0))

    def slide_left(self) -> _T:
        """
        Translate this surface 25 units to the left.
        """
        return self.translate_x(-25)

    def slide_right(self) -> _T:
        """
        Translate this surface 25 units to the right.
        """
        return self.translate_x(25)
