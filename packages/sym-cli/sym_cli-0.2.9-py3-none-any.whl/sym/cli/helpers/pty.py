import os
import pty
from typing import Sequence

from sym.shared.cli.helpers.contexts import push_envs
from sym.shared.cli.helpers.keywords_to_options import Argument, keywords_to_options
from sym.shared.cli.helpers.tee import Tee

from sym.cli.saml_clients.saml_client import SAMLClient


def read_fn(client, args, *, fd_name):
    if client.log_dir:
        with Tee(client.log_dir, f"{args[0]}.{fd_name}") as tee:
            path = tee.path
        file = path.open("wb")
    else:
        file = None

    def reader(fd):
        data = os.read(fd, 1024)
        if file:
            file.write(data)
        return data

    return reader


def spawn(client: SAMLClient, args: Sequence[Argument]):
    master_read = read_fn(client, args, fd_name="stdout")
    stdin_read = read_fn(client, args, fd_name="stdin")
    with push_envs(client.get_creds()):
        pty.spawn(["bash", "-c", *keywords_to_options(args)], master_read, stdin_read)
