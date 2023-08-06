"""Console script for metamock."""

import os
import sys

import click

from .config import write_config
from .server import USER_CONFIG_FILENAME, Server
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"


@click.group("metamock")
@click.version_option(message=header)
@click.option(
    "-c",
    "--config_file",
    type=click.Path(dir_okay=False),
    help=f"config file [~./{USER_CONFIG_FILENAME}]",
)
@click.option(
    "-h", "--host", type=str, help="override config file host address"
)
@click.option("-p", "--port", type=int, help="override config file port")
@click.option("-d", "--debug", is_flag=True, help="debug mode")
@click.pass_context
def cli(ctx, **kwargs):
    class Context:
        def __init__(self, args):
            for k, v in args.items():
                setattr(self, k, v)

    ctx.obj = Context(kwargs)

    def exception_handler(
        exception_type, exception, traceback, debug_hook=sys.excepthook
    ):

        if ctx.obj.debug:
            debug_hook(exception_type, exception, traceback)
        else:
            click.echo(f"{exception_type.__name__}: {exception}", err=True)

    sys.excepthook = exception_handler


@cli.command()
@click.option("-n", "--profile_name", type=str, help="configuration profile")
@click.option("-s", "--server", type=str, help="optional WSGI server name")
@click.pass_context
def run(ctx, profile_name, server):
    """serve mocked aws instance metadata"""

    click.echo(f"metamock {__version__} - serve mocked AWS instance metadata")

    args = ctx.obj
    config_file = args.config_file
    debug = args.debug
    host = args.host
    port = args.port
    return Server(config_file, profile_name, debug).run(host, port, server)


@cli.command()
@click.option("-i", "--id", "_id", type=str, help="AWS_ACCESS_KEY_ID")
@click.option("-k", "--key", type=str, help="AWS_SECRET_ACCESS_KEY")
@click.option("-r", "--region", type=str, help="AWS_REGION")
@click.option("-e", "--mfa_enable", is_flag=True, help="MFA enable")
@click.option("-s", "--mfa_secret", type=str, help="MFA secret")
@click.option(
    "-d", "--mfa_token_duration", type=int, help="MFA token duration"
)
@click.option("-a", "--mfa_role_arn", type=str, help="MFA role ARN")
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def configure(
    ctx,
    _id,
    key,
    region,
    mfa_enable,
    mfa_secret,
    mfa_token_duration,
    mfa_role_arn,
    output,
):
    """write a config file using provided arguments"""

    args = ctx.obj
    id_name = "AWS_ACCESS_KEY_ID"
    key_name = "AWS_SECRET_ACCESS_KEY"
    region_name = "AWS_REGION"

    return write_config(
        output,
        args.host or "0.0.0.0",
        args.port or 80,
        _id or os.environ.get(id_name, "SET_" + id_name),
        key or os.environ.get(key_name, "SET_" + key_name),
        region or os.environ.get(region_name, "SET_" + region_name),
        mfa_enable,
        mfa_secret,
        mfa_token_duration,
        mfa_role_arn,
    )
    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
