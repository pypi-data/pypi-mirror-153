import sys

import click

from sifflet import __version__
from sifflet.configure.commands import configure
from sifflet.configure.service import ConfigureService
from sifflet.constants import SIFFLET_CONFIG_CTX
from sifflet.errors import exception_handler
from sifflet.ingest.commands import ingest
from sifflet.rules.commands import rules
from sifflet.status.commands import status


@exception_handler
def main():
    """Entrypoint"""
    sys.exit(sifflet_cli())  # pylint: disable=E1120


@click.group()
@click.version_option(__version__)
@click.option("--debug", is_flag=True, hidden=True)
@click.option("--dev", "dev_mode", is_flag=True, hidden=True)
@click.pass_context
def sifflet_cli(ctx, debug: bool, dev_mode: bool):
    """Sifflet CLI"""
    sifflet_config = ConfigureService().load_configuration(debug, dev_mode)
    ctx.ensure_object(dict)
    ctx.obj[SIFFLET_CONFIG_CTX] = sifflet_config


sifflet_cli.add_command(status)
sifflet_cli.add_command(configure)
sifflet_cli.add_command(rules)
sifflet_cli.add_command(ingest)
