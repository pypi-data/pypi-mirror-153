import json
import sys
import traceback
from functools import wraps, partial

from requests.exceptions import InvalidURL, RequestException
from rich import print as rich_print
from urllib3.exceptions import LocationParseError, HTTPError

from sifflet.apis.client import ApiException
from sifflet.configure.service import ConfigureService
from sifflet.constants import TENANT_KEY_OS, TOKEN_KEY_OS
from sifflet.logger import logger


class SiffletConfigError(Exception):
    """Raised when missing an environment variable"""


def exception_handler(func):
    if not func:
        return partial(exception_handler)

    @wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (InvalidURL, LocationParseError) as err:
            rich_print(f"Unable to parse url, please check the configuration of your tenant name. {err}")
        except (HTTPError, RequestException) as err:
            logger.warning(err)
        except ApiException as err:
            error_body = json.loads(err.body)
            logger.debug(err)
            logger.error(
                f"{err.status} - {error_body['title'] if 'title' in error_body else ''} -"
                f" {error_body['detail'] if 'detail' in error_body else ''}"
            )
        except Exception as err:  # pylint: disable=W0703
            logger.debug(traceback.format_exc())
            logger.error(err)
        return None

    return inner_function


def config_needed_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sifflet_config_ = args[1]
        sifflet_config = ConfigureService().load_configuration(
            dev_mode=sifflet_config_.dev_mode, debug=sifflet_config_.debug, previous_config=sifflet_config_
        )

        if sifflet_config is None or not sifflet_config.token and not sifflet_config.tenant:
            logger.error(
                f"The environment variables [italic]{TENANT_KEY_OS}[/] and [italic]{TOKEN_KEY_OS}[/] must be set. "
                "You can also configure credentials using [bold]sifflet configure[/bold]"
            )
            sys.exit(1)
        elif not sifflet_config.token:
            logger.error(
                f"The environment variable [italic]{TOKEN_KEY_OS}[/] must be set. "
                "You can also configure it using [bold]sifflet configure[/bold]"
            )
            sys.exit(1)
        elif not sifflet_config.tenant:
            logger.error(
                f"The environment variable [italic]{TENANT_KEY_OS}[/] must be set. "
                "You can also configure it using [bold]sifflet configure[/bold]"
            )
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper
