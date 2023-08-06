import click

from sifflet.constants import SIFFLET_CONFIG_CTX
from sifflet.ingest.service import IngestionService


@click.group()
def ingest():
    """Control ingestion of tools into Sifflet."""


@ingest.command()
@click.option(
    "--project-name",
    "project_name",
    required=True,
    type=str,
    help="The name of your dbt project (in your dbt_project.yml file)",
)
@click.option(
    "--target", type=str, required=True, help="The target value of the profile (in your dbt_project.yml file)"
)
@click.option("--input-folder", "input_folder", required=True, type=str, help="The dbt execution folder")
@click.pass_context
def dbt(ctx, project_name: str, target: str, input_folder: str):
    """
    Ingestion of dbt metadata to Sifflet
    """
    sifflet_config = ctx.obj[SIFFLET_CONFIG_CTX]

    ingestion_service = IngestionService(sifflet_config)
    ingestion_service.ingest_dbt(project_name, target, input_folder)
