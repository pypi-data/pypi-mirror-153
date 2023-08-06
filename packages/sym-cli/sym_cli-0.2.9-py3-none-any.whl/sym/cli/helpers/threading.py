from threading import Condition, Thread
from typing import Callable, Optional, Sequence, Tuple

import click

from sym.cli.errors import CliError


def first(
    values: Sequence[str],
    finder: Callable[[str], str],
    timeout=5,
) -> Optional[Tuple[str, str]]:
    ctx = click.get_current_context()
    results = {}
    cv = Condition()

    def target(val):
        with ctx:
            try:
                res = finder(val)
            except CliError:
                return
            if res:
                with cv:
                    results[val] = res
                    cv.notify()

    for val in values:
        Thread(target=target, args=(val,), daemon=True).start()

    with cv:
        if cv.wait_for(lambda: bool(results), timeout=timeout):
            return list(results.items())[0]
