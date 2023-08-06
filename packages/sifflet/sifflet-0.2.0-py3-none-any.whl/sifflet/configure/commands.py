import click

from sifflet.configure.service import ConfigureService, SiffletConfig
from sifflet.constants import SIFFLET_CONFIG_CTX, TENANT_KEY, TOKEN_KEY
from sifflet.logger import logger


def default_from_context(default_key):
    class DefaultFromContext(click.Option):
        def get_default(self, ctx, call=True):
            sifflet_config: SiffletConfig = ctx.obj[SIFFLET_CONFIG_CTX]
            if default_key == TENANT_KEY:
                self.default = sifflet_config.tenant
            if default_key == TOKEN_KEY:
                self.default = sifflet_config.token
            return super().get_default(ctx)

        def __str__(self):
            print(default_key)
            return "*" * 8 if default_key == TOKEN_KEY else self.default

    return DefaultFromContext


@click.command()
@click.option(
    "--tenant",
    prompt="Your tenant name",
    help="Correspond to the prefix of your sifflet url https://TENANT.siffletdata.com/",
    show_default=True,
    cls=default_from_context(TENANT_KEY),
)
@click.option(
    "--token",
    prompt="Your API access token",
    help="The access token must be generated in the Web UI of Sifflet Settings > Access-Tokens",
    hide_input=True,
    cls=default_from_context(TOKEN_KEY),
)
def configure(tenant: str, token: str):
    """Configure sifflet variables"""
    service = ConfigureService()
    logger.debug("start service")
    sifflet_config = service.configure(tenant, token)
    service.show_configuration(sifflet_config)
