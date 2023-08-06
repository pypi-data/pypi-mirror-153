import requests
from requests import Response

from sifflet.apis.base import BaseApi
from sifflet.apis.client.api import access_token_api
from sifflet.errors import exception_handler
from sifflet.logger import logger


class ApiStatus(BaseApi):
    def __init__(self, sifflet_config):
        super().__init__(sifflet_config)
        self.api_instance = access_token_api.AccessTokenApi(self.api)

    @exception_handler
    def fetch_health_tenant(self) -> bool:
        logger.debug(f"Check heath tenant = {self.host}")
        path: str = f"{self.host}/actuator/health"
        response: Response = requests.get(path)
        return response.status_code == 200

    @exception_handler
    def fetch_token_valid(self) -> bool:
        logger.debug(f"Check token for host = {self.host}")
        return self.api_instance.access_token_validity(authorization=self.sifflet_config.token)
