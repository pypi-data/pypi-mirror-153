from airflow.models.baseoperator import BaseOperator

from sifflet.ingest.service import IngestionService


class DbtIngestOperator(BaseOperator):
    ui_color = "#113e60"
    ui_fgcolor = "#000000"

    def __init__(self, project_name: str, target: str, input_folder: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.project_name = project_name
        self.target = target
        self.input_folder = input_folder

    def execute(self, context):
        IngestionService(sifflet_config=None).ingest_dbt(self.project_name, self.target, self.input_folder)
        return True
