import shlex
import subprocess
import sys
from functools import wraps
from subprocess import PIPE, CalledProcessError
from typing import Any, Callable, Iterator, Optional, Sequence, TypeVar, cast

import click
from sym.shared.cli.decorators import (  # noqa
    command_require_bins,
    require_bins,
    retry,
    setup_segment,
    setup_sentry,
)
from sym.shared.cli.errors import (
    CliError,
    ErrorPatterns,
    FailedSubprocessError,
    SuppressedError,
    raise_if_match,
)
from sym.shared.cli.helpers.keywords_to_options import Argument, keywords_to_options
from sym.shared.cli.helpers.tee import Tee

from sym.cli.helpers.config import Config
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

F = TypeVar("F", bound=Callable[..., Any])


def run_subprocess(
    func: Callable[..., Iterator[Sequence[Argument]]]
) -> Callable[..., Optional[Sequence[Optional[str]]]]:
    @wraps(func)
    def impl(
        *args: Any,
        censor_: bool = False,
        capture_output_: bool = False,
        silence_stderr_: bool = True,
        input_: str = None,
        run_subprocess_options_: Optional[GlobalOptions] = None,
        **kwargs: Any,
    ) -> Optional[Sequence[Optional[str]]]:

        options = run_subprocess_options_
        if not options:
            # Ideally we will never need to access click at this level and
            # will instead always pass in options. This is for backward
            # compatibility as we refactor.
            options = click.get_current_context().find_object(GlobalOptions)

        outputs = []
        tee = bool(options.log_dir) and not censor_

        for command in func(*args, **kwargs):
            command = keywords_to_options(command)
            options.dprint(f"exec: {shlex.join(command)}\n")
            if tee:
                command = Tee.tee_command(options.log_dir, command)
            result = subprocess.run(
                command,
                check=True,
                capture_output=capture_output_,
                input=input_,
                stderr=None if (capture_output_ or not silence_stderr_) else PIPE,
                text=True,
                shell=tee,
                executable="/bin/bash" if tee else None,
            )
            outputs.append(result.stdout)
            if not censor_:
                options.dprint(result.stdout)
        if capture_output_:
            return outputs

    return impl


def intercept_errors(
    patterns: ErrorPatterns = {},
    *,
    quiet: bool = False,
    suppress: bool = False,
) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(
            *args: Any,
            quiet_: bool = False,
            suppress_: bool = False,
            intercept_errors_options_: Optional[GlobalOptions] = None,
            **kwargs: Any,
        ) -> Any:

            options = intercept_errors_options_
            if not options:
                # Ideally we will never need to access click at this level and
                # will instead always pass in options. This is for backward
                # compatibility as we refactor.
                options = click.get_current_context().find_object(GlobalOptions)

            try:
                return fn(*args, **kwargs)
            except CalledProcessError as err:
                message = err.stderr or ""
                raise_if_match(patterns, message)
                if not (quiet or quiet_):
                    sys.stderr.write(message)
                else:
                    options.dprint(message)
                if suppress or suppress_:
                    raise SuppressedError(err) from err
                else:
                    raise FailedSubprocessError(err) from err

        return cast(F, wrapped)

    return decorate


def loses_interactivity(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        if resource := kwargs.get("resource"):
            saml_client = SAMLClientFactory.create_saml_client(
                resource, context.find_object(GlobalOptions)
            )
            saml_client.ensure_session()
        return context.invoke(fn, *args, **kwargs)

    return cast(F, require_login(wrapped))


def skip_analytics(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        options = context.ensure_object(GlobalOptions)
        options.disable_analytics = True
        return context.invoke(fn, *args, **kwargs)

    return cast(F, wrapped)


def require_login(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        if not Config.is_logged_in():
            raise CliError("Please run `sym login` first")
        return context.invoke(fn, *args, **kwargs)

    return cast(F, wrapped)
