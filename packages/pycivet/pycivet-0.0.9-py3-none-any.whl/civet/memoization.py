"""
Manual control of memoization features.
"""

from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import ContextManager, Sequence, Callable, NewType

from civet.abstract_data import AbstractDataCommand
from civet.shells import Shell, subprocess_run

_IntermediatePath = NewType('IntermediatePath', Path)


@dataclass(frozen=True)
class Memoizer:
    """
    A `Memoizer` executes `civet.abstract_data.AbstractDataCommand` and
    writes their outputs to temporary paths. These outputs are cached,
    so that when given the same `civet.abstract_data.AbstractDataCommand`
    to run again, its cached output is returned.

    ### Dependency Tree

    `civet.abstract_data.AbstractDataCommand.command` produces a sequence
    which usually contain other `AbstractDataCommand`.
    These nested objects are dependencies which need to be computed first.
    Hence, `AbstractDataCommand` can be thought of as
    nodes of a *dependency tree* where the root is the desired output and the
    leaves are input files. `Memoizer` performs DFS on the tree, executing
    the commands represented by each node, to produce the intermediate outputs
    necessary to compute the root.
    """

    temp_dir: Path
    shell: Shell
    require_output: bool = True
    _cache: dict[AbstractDataCommand, _IntermediatePath] = field(init=False, default_factory=dict)

    def save(self, d: AbstractDataCommand, output: str | PathLike) -> None:
        """
        If `d` was previously computed, copy the cached result to `output`.
        Else, compute `d`, cache the result, and copy to `output`.
        """
        if d not in self._cache:
            self._force_save(d)
        self.shell(('cp', '-r', self._cache[d], output))

    def _force_save(self, d: AbstractDataCommand) -> _IntermediatePath:
        """
        Compute `d` and cache the result.
        """
        output = self.__temp(d.preferred_suffix)
        cmd = self._resolve_command(d.command(output))
        self.shell(cmd)
        if self.require_output and not output.exists():
            print(f'output is: {output}')
            self.shell(('ls', self.temp_dir))
            raise NoOutputError(d)
        self._cache[d] = output
        return output

    def _cache_hit(self, d: AbstractDataCommand) -> _IntermediatePath:
        """
        If `d` was previously computed, return the path to its cached result.
        Else, compute `d` first and then return the path to its cached result.
        """
        if d in self._cache:
            return self._cache[d]
        return self._force_save(d)

    def _resolve_command(self, cmd: Sequence[str | PathLike | AbstractDataCommand]) -> Sequence[str | PathLike]:
        """
        Replace every `AbstractDataCommand` in `cmd` with a path to their cached output.
        The `AbstractDataCommand` will be computed if it was not computed before.
        """
        return tuple(self._resolve_component(c) for c in cmd)

    def _resolve_component(self, c: str | PathLike | AbstractDataCommand) -> str | PathLike:
        if isinstance(c, (str, PathLike)):
            return c
        elif isinstance(c, AbstractDataCommand):
            return self._cache_hit(c)
        # TODO subshell support
        raise TypeError(f'{c} is not a [str | PathLike | AbstractDataCommand]')

    def __temp(self, suffix='') -> _IntermediatePath:
        """
        Create a temporary path name.
        """
        with NamedTemporaryFile(suffix=suffix, dir=self.temp_dir) as t:
            pass
        return _IntermediatePath(Path(t.name))


@dataclass(frozen=True)
class Session(ContextManager[Memoizer]):
    """
    A `Session` manages the temporary directory of a `Memoizer`.
    """

    require_output: bool = True
    """
    If True, raise `NoOutputError` if a command fails to produce output to its given path.
    """
    shell: Shell = subprocess_run
    """
    A function which executes its parameters as a subprocess.
    """
    temp_dir: ContextManager[str] = field(default_factory=TemporaryDirectory)

    def __enter__(self) -> Memoizer:
        temp_dir_name = self.temp_dir.__enter__()
        return Memoizer(Path(temp_dir_name), require_output=self.require_output, shell=self.shell)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_dir.__exit__(exc_type, exc_val, exc_tb)


class NoOutputError(Exception):
    """
    Raised when a subprocesses ran by `Memoizer` does not create its output given path.
    """
    pass
