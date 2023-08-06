import configparser
import logging
import os
from dataclasses import dataclass
from pathlib import Path

from sifflet.constants import (
    TENANT_KEY,
    TOKEN_KEY,
    DEV_MODE_KEY,
    DEBUG_KEY,
    APP_SECTION_KEY,
    TENANT_KEY_OS,
    TOKEN_KEY_OS,
)
from sifflet.logger import logger


@dataclass
class SiffletConfig:
    tenant: str
    token: str
    debug: bool = False
    dev_mode: bool = False


class ConfigureService:
    path_folder_config = Path.home() / ".sifflet"
    path_file_config = path_folder_config / "config.ini"

    def configure(self, tenant, token) -> SiffletConfig:
        sifflet_config = SiffletConfig(
            tenant=tenant,
            token=token,
        )

        config = configparser.ConfigParser()
        config[APP_SECTION_KEY] = {
            TENANT_KEY: sifflet_config.tenant,
            TOKEN_KEY: sifflet_config.token,
            DEV_MODE_KEY: sifflet_config.dev_mode,
            DEBUG_KEY: sifflet_config.debug,
        }

        self.path_folder_config.mkdir(exist_ok=True, parents=True)

        with open(self.path_file_config, mode="w", encoding="utf-8") as configfile:
            config.write(configfile)

        return sifflet_config

    def load_configuration(self, debug=False, dev_mode=False, previous_config: SiffletConfig = None) -> SiffletConfig:
        """
        Initialize Sifflet configuration
        First from environment variables then falls back to configuration file
        """
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Log level set to DEBUG")

        config = configparser.ConfigParser()
        config.read(self.path_file_config)

        # Get env var or falls back to config file
        if "APP" in config.sections():
            default_tenant = config[APP_SECTION_KEY][TENANT_KEY]
            default_token = config[APP_SECTION_KEY][TOKEN_KEY]
        elif previous_config:
            default_tenant = previous_config.tenant or ""
            default_token = previous_config.token or ""
        else:
            default_tenant = ""
            default_token = ""
        return SiffletConfig(
            tenant=os.getenv(TENANT_KEY_OS, default=default_tenant),
            token=os.getenv(TOKEN_KEY_OS, default=default_token),
            dev_mode=dev_mode,
            debug=debug,
        )

    @staticmethod
    def show_configuration(sifflet_config: SiffletConfig):
        logger.info(f'Current config is \nTENANT="{sifflet_config.tenant}"')
