"""
Wrappers around
[`subprocess.run`](https://docs.python.org/3/library/subprocess.html#subprocess.run).
"""

import subprocess as sp
from os import PathLike
from typing import Sequence, Callable

Shell = Callable[[Sequence[str | PathLike]], None]


def subprocess_run(cmd: Sequence[str | PathLike]) -> None:
    """
    Alias for `subprocess.run(cmd, check=True)`
    """
    sp.run(cmd, check=True)


def quiet(cmd: Sequence[str | PathLike]) -> None:
    """
    Similar to `subprocess_run` but output streams are piped to `/dev/null`.
    """
    sp.run(cmd, check=True, stdout=sp.DEVNULL, stderr=sp.STDOUT)
