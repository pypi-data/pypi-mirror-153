from sifflet.apis import client
from sifflet.configure.service import SiffletConfig
from sifflet.errors import config_needed_handler

DEFAULT_PAGE_NUM = 0
DEFAULT_ITEMS_PER_PAGE = 15


class BaseApi:
    @config_needed_handler
    def __init__(self, sifflet_config: SiffletConfig):
        self.sifflet_config = sifflet_config
        if sifflet_config.dev_mode:
            self.host = f"http://{sifflet_config.tenant}"
        else:
            self.host = f"https://{self.sifflet_config.tenant}api.siffletdata.com"
        configuration = client.Configuration(host=self.host, access_token=self.sifflet_config.token)
        self.api = client.ApiClient(configuration)
