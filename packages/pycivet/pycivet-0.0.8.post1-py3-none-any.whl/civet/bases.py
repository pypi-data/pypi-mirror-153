"""
Base classes for file types.
"""
import abc
from os import PathLike
from typing import Sequence, TypeVar, Generic, Callable
from dataclasses import dataclass
from civet.abstract_data import AbstractDataCommand
from civet.memoization import Session
from civet.shells import Shell, subprocess_run


@dataclass(frozen=True)
class DataSource(AbstractDataCommand, abc.ABC):
    """
    A `DataSource` provides the `DataSource.save` method to `civet.abstract_data.AbstractDataCommand`,
    which is an alias for typical usage of `civet.memoization.Session`.
    """
    def save(self, output: str | PathLike,
             require_output: bool = True,
             shell: Shell = subprocess_run) -> None:
        r"""
        Save the result of this command to the given output path.

        The behavior of `save` can be customized by specifying `shell` as different
        wrappers around `subprocess.run`. For example, to save the logs of subprocesses:

        ```python
        from pathlib import Path
        import subprocess as sp

        log_path = Path('output.log')
        with log_path.open('wb') as log_file:
            def saves_log_shell(cmd):
                log_file.write(b'Running: ')
                log_file.write(str(cmd).encode('utf-8'))
                log_file.write(b'\n')
                log_file.flush()
                sp.run(cmd, stdout=log_file, stderr=sp.STDOUT, check=True)
            GenericSurface('input.obj').slide_left().save('lefter.obj', shell=saves_log_shell)
        ```
        """
        with Session(require_output, shell) as s:
            s.save(self, output)


_D = TypeVar('_D', bound='DataFile')


@dataclass(frozen=True)
class DataFile(DataSource, Generic[_D], abc.ABC):
    """
    A `DataFile` represents a file type. It can wrap input files of that file type,
    or commands which produce results of that file type.
    """

    input: str | PathLike | AbstractDataCommand

    def command(self, output: str | PathLike) -> Sequence[str | PathLike | AbstractDataCommand]:
        return 'cp', self.input, output

    def create_command(self, command: Callable[[str | PathLike], Sequence[str | PathLike | AbstractDataCommand]]
                       ) -> _D:
        """
        Chain a command which produces output of the same type as this `DataFile`.
        """
        class Intermediate(self.__class__):
            def command(self, output: str | PathLike) -> Sequence[str | PathLike | AbstractDataCommand]:
                return command(output)
        return Intermediate(self)
