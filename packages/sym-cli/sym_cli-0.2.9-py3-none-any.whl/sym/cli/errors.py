from typing import Sequence

import click
from click import Argument, BadParameter, Option
from sym.shared.cli.errors import (  # noqa
    BotoError,
    CliError,
    CliErrorWithHint,
    FailedSubprocessError,
    OfflineError,
    SuppressedError,
    UnknownError,
    WrappedSubprocessError,
    raise_if_match,
)
from sym.shared.cli.helpers.keywords_to_options import keywords_to_options
from sym.shared.cli.helpers.util import get_param


class UnavailableResourceError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have permission to access the Sym resource you requested.",
            "Request approval and then try again.",
        )


class ResourceNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The Sym resource you requested is not set up properly.",
            "Contact your Sym administrator.",
            report=True,
        )


class TargetNotConnected(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The instance you tried to SSH into is not connected to AWS Session Manager.",
            "Ask your Sym administrator if they've set up Session Manager.",
        )


class AccessDenied(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have access to connect to this instance.",
            "Have you requested access?",
        )


class InstanceNotFound(CliError):
    def __init__(self, instance) -> None:
        super().__init__(f"Could not find instance {instance}")


class SAMLClientNotFound(CliError):
    def __init__(self) -> None:
        super().__init__(
            "No valid SAML client found in PATH. Supported clients are listed in `sym --help`."
        )


class MissingPublicKey(WrappedSubprocessError):
    def __init__(self, wrapped, user) -> None:
        super().__init__(wrapped, f"Does the user ({user}) exist on the instance?")


class SamlClientNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "Your SAML client is not set up.",
            "Consult the docs for your client.",
        )


class ExpiredCredentials(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "Your AWS credentials have expired.",
            "\n".join(
                [
                    "Try running `sym write-creds` again, or run your command with SYM_SESSION_LENGTH=60.",
                    "For more details, see: https://docs.symops.com/docs/common-issues-sym-cli#error-your-aws-credentials-have-expired",
                ]
            ),
        )


class MissingResource(CliErrorWithHint, BadParameter):
    def __init__(
        self,
        profiles: Sequence[str],
        resource_name="resource",
    ) -> None:
        super().__init__(
            "You must supply a resource!",
            self.__class__.gen_hint(resource_name, profiles),
        )

    @classmethod
    def gen_hint(cls, resource_name, profiles) -> str:
        return "\n".join(
            [
                click.style(
                    f"These are the {resource_name}s available to you:",
                    fg="white",
                    reset=False,
                ),
                *[f"  - {key}" for key in profiles],
            ]
        )


class InvalidResource(CliErrorWithHint, BadParameter, KeyError):
    def __init__(
        self,
        resource: str,
        profiles: Sequence[str],
        resource_name="resource",
    ) -> None:
        super().__init__(
            f"Invalid {resource_name} name '{resource}'",
            self.gen_hints(resource, resource_name, profiles),
        )

    def gen_hints(self, resource, resource_name, profiles) -> Sequence[str]:
        hints = [
            "\n".join(
                [
                    f"Has your Sym Implementer set up {resource} yet?",
                    MissingResource.gen_hint(resource_name, profiles),
                ]
            )
        ]
        if ctx := click.get_current_context():
            if ctx.command.params[0].name == resource_name:
                args = [
                    v
                    for k, v in ctx.params.items()
                    if isinstance(get_param(ctx.command, k), Argument)
                ]
                if len(args) == 1:
                    return hints
                opts = {
                    k: v
                    for k, v in ctx.params.items()
                    if isinstance(get_param(ctx.command, k), Option)
                    and get_param(ctx.command, k).get_default(ctx) != v
                }
                cmd = " ".join(
                    [
                        *keywords_to_options([opts]),
                        (
                            click.style(profiles[0], fg="magenta", reset=False)
                            + click.style("", fg="white", reset=False)
                        ),
                        *keywords_to_options(args),
                        *ctx.args,
                    ]
                )
                hints.insert(
                    0,
                    "\n".join(
                        [
                            "Did you forget to pass a RESOURCE as the first argument?",
                            click.style(
                                f"e.g. `{ctx.command_path} {cmd}`",
                                fg="white",
                            ),
                        ]
                    ),
                )

        return hints
