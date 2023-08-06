from typing import List

from rich.console import Console
from rich.table import Table, Column

from sifflet.logger import logger


def show_table(table: List[dict], title: str = None):
    """Utility to display rich tables"""

    if table:
        header = list(table[0].keys())

        if "id" in header:
            header = filter(lambda x: x != "id", header)
            table_formatted = Table(Column(header="id", no_wrap=True), *header)
        else:
            table_formatted = Table(*header)

        for val in table:
            table_formatted.add_row(*val.values())

        table_formatted.title = title

        console = Console()
        console.print(table_formatted)
    else:
        logger.warning("No data to display")
