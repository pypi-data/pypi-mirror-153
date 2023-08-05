"""Console script for metamock."""

import sys

import click

from .config import write_config
from .server import Server
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"


@click.command("metamock")
@click.version_option(message=header)
@click.option("-d", "--debug", is_flag=True, help="debug mode")
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    help="config file (default ~./metamock/config)",
)
@click.option("-h", "--host", type=str, default="169.254.169.254")
@click.option("-p", "--port", type=int, default=45000)
@click.option(
    "-P", "--profile", type=str, help="name of the profile to load by default"
)
@click.option(
    "-i", "--id", "key_id", type=str, help="configure: AWS_ACCESS_KEY_ID"
)
@click.option("-k", "--key", type=str, help="configure: AWS_SECRET_ACCESS_KEY")
@click.option("-r", "--region", type=str, help="configure: AWS_REGION")
@click.argument("command", type=str, default="server")
def cli(debug, config, host, port, profile, key_id, key, region, command):
    """serve mocked aws instance metadata

    Commands:

        configure: generate a config file at ~/.metamock/config

        server: run the server

    """

    def exception_handler(
        exception_type, exception, traceback, debug_hook=sys.excepthook
    ):

        if debug:
            debug_hook(exception_type, exception, traceback)
        else:
            click.echo(f"{exception_type.__name__}: {exception}", err=True)

    sys.excepthook = exception_handler

    click.echo(
        f"metamock {__version__} - because dev systems need 169.254.169.254 too."
    )

    if command == "configure":
        return write_config(
            key_id or "AWS_SECRET_KEY_ID",
            key or "AWS_SECRET_ACCESS_KEY",
            region or "AWS_REGION",
        )
    else:
        return Server(config, host, port, profile).run()


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
