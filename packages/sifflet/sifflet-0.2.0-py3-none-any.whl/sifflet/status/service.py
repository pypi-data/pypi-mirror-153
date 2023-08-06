import datetime
from typing import Dict

import jwt
from jwt.exceptions import InvalidTokenError
from rich import print as rich_print

from sifflet.configure.service import SiffletConfig
from sifflet.errors import exception_handler
from sifflet.logger import logger
from sifflet.status.api import ApiStatus


class StatusService:
    def __init__(self, sifflet_config):
        self.sifflet_config: SiffletConfig = sifflet_config
        self.api_rules = ApiStatus(sifflet_config)

    @exception_handler
    def check_status(self):
        tenant_validity = self._check_tenant()

        token_validity = self._check_token() if tenant_validity else False

        if token_validity and tenant_validity:
            rich_print("[bold green]Status = OK[/bold green]")
        else:
            rich_print("[bold red]Status = KO[/bold red]")

    @exception_handler
    def _check_token(self):
        token_validity = False
        try:
            decoded_token: Dict = jwt.decode(self.sifflet_config.token, options={"verify_signature": False})
            expiration_time: datetime = datetime.datetime.fromtimestamp(decoded_token.get("exp"))
            rich_print(f"Token expiration date = {expiration_time}")
            token_validity = self.api_rules.fetch_token_valid()
        except InvalidTokenError as err:
            rich_print(f"[red]Error decoding token:[/] {err}")

        if token_validity:
            rich_print("[green]Token is valid with scope API[/green]")
        else:
            rich_print("[red]Token is not valid[/red]")

        return token_validity

    @exception_handler
    def _check_tenant(self):
        logger.debug(f"Tenant is set to: {self.sifflet_config.tenant}")
        tenant_validity = self.api_rules.fetch_health_tenant()

        if tenant_validity:
            logger.debug(f"Connected to tenant: {self.sifflet_config.tenant}")
            rich_print("[green]Tenant is up and reachable[/green]")
        else:
            logger.debug(f"Can't connect to tenant named: {self.sifflet_config.tenant}")
            rich_print("[red]Tenant is not reachable. Please check the configuration of your tenant name[/red]")

        return tenant_validity
