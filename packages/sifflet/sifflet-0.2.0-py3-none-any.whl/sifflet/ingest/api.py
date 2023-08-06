from pathlib import Path

import requests

from sifflet.apis.base import BaseApi
from sifflet.apis.client.api import dbt_controller_api
from sifflet.errors import exception_handler
from sifflet.logger import logger


class ApiIngestion(BaseApi):
    def __init__(self, sifflet_config):
        super().__init__(sifflet_config)
        self.api_instance = dbt_controller_api.DbtControllerApi(self.api)

    @exception_handler
    def send_dbt_metadata(self, project_name, target, input_folder: str) -> None:
        logger.debug(f"Sending dbt metadata to host = {self.host}")
        catalog_file = Path(input_folder) / "target" / "catalog.json"
        run_results = Path(input_folder) / "target" / "run_results.json"
        manifest_file = Path(input_folder) / "target" / "manifest.json"

        path_files = {
            "catalog": open(catalog_file, "rb"),
            "run_results": open(run_results, "rb"),
            "manifest": open(manifest_file, "rb"),
        }

        # Use requests instead of generated client avoid
        # {"title":"Bad Request","status":400,"detail":"Current request is not a multipart request"}
        # thrown by the backend
        res = requests.post(
            url=f"{self.host}/api/v1/metadata/dbt/{project_name}/{target}",
            files=path_files,
            headers={"Authorization": f"Bearer {self.sifflet_config.token}"},
        )
        res.raise_for_status()
        logger.debug(res.status_code)

        # files = {
        #     "catalog": open(catalog_file, "r"),
        #     "run_results": open(run_results, "r"),
        #     "manifest": open(manifest_file, "r"),
        # }
        # self.api_instance.upload_metadata_files(
        #     project_name=project_name, target=target, inline_object=files, _content_type='multipart/form-data'
        # )
