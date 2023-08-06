"""
Defines types and operations related to MINC files.
"""
from dataclasses import dataclass
from os import PathLike
from typing import Literal, TypeVar, Generic, Optional

from civet.bases import DataFile
from civet.extraction.kernels import ngh_count_kernel

_M = TypeVar('_M', bound='GenericMinc')
_V = TypeVar('_V', bound='GenericMinc')


@dataclass(frozen=True)
class GenericMinc(DataFile[_M], Generic[_M]):

    preferred_suffix = '.mnc'

    def mincresample(self, like_volume: _V) -> _V:
        def command(output):
            return (
                'mincresample', '-clobber', '-quiet',
                '-like', like_volume, self, output
            )
        return like_volume.create_command(command)

    def reshape255(self) -> 'GenericMask':
        def command(output):
            return (
                'mincreshape', '-quiet', '-clobber', '-unsigned', '-byte',
                '-image_range', '0', '255', '-valid_range', '0', '255',
                self, output
            )
        return GenericMask(self).create_command(command)

    def resamplef64(self, *extra_flags: str) -> 'GenericFloatMinc':
        def command(output):
            return 'mincresample', '-quiet', '-double', *extra_flags, self, output
        return GenericFloatMinc(self).create_command(command)


_MA = TypeVar('_MA', bound='GenericMask')


class GenericMask(GenericMinc[_MA], Generic[_MA]):

    def dilate_volume(self, dilation_value: int, neighbors: Literal[6, 26], n_dilations: int) -> _MA:
        def command(output):
            return (
                'dilate_volume', self, output,
                str(dilation_value), str(neighbors), str(n_dilations)
            )
        return self.create_command(command)

    def minccalc_u8(self, expression: str, *other_volumes: 'GenericMask') -> _MA:
        def command(output):
            return (
                'minccalc', '-clobber', '-quiet',
                '-unsigned', '-byte',
                '-expression', expression,
                self, *other_volumes, output
            )
        return self.create_command(command)

    def mincdefrag(self, label: int, stencil: Literal[6, 19, 27], max_connect: Optional[int] = None) -> _MA:
        def command(output):
            cmd = ['mincdefrag', self, output, str(label), str(stencil)]
            if max_connect is not None:
                cmd.append(str(max_connect))
            return cmd
        return self.create_command(command)

    def reshape_bbox(self) -> _MA:
        def command(output):
            return 'mincreshape_bbox_helper', self, output
        return self.create_command(command)

    def mincmorph_convolve_u8(self, kernel: str | PathLike = ngh_count_kernel) -> _MA:
        def command(output):
            return (
                'mincmorph',
                '-unsigned', '-byte',
                '-convolve',
                '-kernel', kernel,
                self, output
            )
        return self.create_command(command)


class Mask(GenericMask['Mask']):
    """
    A `Mask` represents a volume (`.mnc`) with discrete intensities (segmentation volume or brain mask).
    """
    pass


_F = TypeVar('_F', bound='GenericFloatMinc')


class GenericFloatMinc(GenericMinc[_F], Generic[_F]):
    def mincblur(self, fwhm: float) -> _F:
        # result is not a binary mask, it has float values in [0, 1],
        # maybe define a unique type?
        def command(output):
            return 'mincblur_correct_name.sh', '-quiet', '-fwhm', str(fwhm), self, output
        return self.create_command(command)


class FloatMinc(GenericFloatMinc['FloatMinc']):
    pass
