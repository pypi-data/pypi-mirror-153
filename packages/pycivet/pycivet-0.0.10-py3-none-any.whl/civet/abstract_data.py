"""
Abstraction of command-line programs which produce data files.
"""
import abc
from os import PathLike
from typing import Sequence, Union


class AbstractDataCommand(abc.ABC):
    """
    An `AbstractDataCommand` represents a command-line program which can produce
    output data to a given path.

    Subclasses of `AbstractDataCommand` must be
    [hashable](https://docs.python.org/3/library/typing.html#typing.Hashable)
    and immutable, because `AbstractDataCommand` objects are used as dictionary
    keys by `civet.memoization.Memoizer`. It's recommended to use
    [frozen dataclasses](https://docs.python.org/3/library/dataclasses.html#frozen-instances).
    """

    @abc.abstractmethod
    def command(self, output: str | PathLike) -> Sequence[Union[str, PathLike, 'AbstractDataCommand']]:
        ...

    @property
    def preferred_suffix(self) -> str:
        """
        Preferred output path suffix for this command.
        """
        return ''
