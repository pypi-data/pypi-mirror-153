import click
from rich import print as rich_print

from sifflet import __version__
from sifflet.constants import SIFFLET_CONFIG_CTX
from sifflet.status.service import StatusService


@click.command()
@click.pass_context
def status(ctx):
    """
    Display basic status of sifflet cli
    """
    sifflet_config = ctx.obj[SIFFLET_CONFIG_CTX]

    show_status: str = f"""
Sifflet version = {__version__}
Tenant = {sifflet_config.tenant}"""

    rich_print(show_status)

    status_service = StatusService(sifflet_config)
    status_service.check_status()
