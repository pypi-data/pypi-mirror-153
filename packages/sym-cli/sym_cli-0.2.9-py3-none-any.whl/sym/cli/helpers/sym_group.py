from typing import Any, Callable

from sym.shared.cli.errors import get_active_env_vars
from sym.shared.cli.helpers.sym_group import AutoTagCommand as SharedAutoTagCommand
from sym.shared.cli.helpers.sym_group import SymGroup as SharedSymGroup

from ..saml_clients.chooser import choose_saml_client


class AutoTagCommand(SharedAutoTagCommand):
    def parse_args(self, ctx, args):
        """
        To work around https://github.com/pallets/click/issues/714, we are doing a trick:
        we always parse a resource *option* from the root command, and then we sometimes
        rewrite the args passed to a child command before parsing the resource *argument*.
        """
        if (
            self.params
            and (resource := ctx.parent.params.get("resource"))
            and self.params[0].name == "resource"
            and (
                not args
                or not choose_saml_client(
                    ctx.parent.params["saml_client_name"]
                ).validate_resource(args[0])
            )
        ):
            args = [resource] + args
        return super().parse_args(ctx, args)

    def format_epilog(self, ctx, formatter):
        if not self.epilog:
            formatter.write(get_active_env_vars())
        super().format_epilog(ctx, formatter)


class SymGroup(SharedSymGroup):
    def command(
        self, *args: Any, cls=None, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=cls or AutoTagCommand)  # type: ignore
