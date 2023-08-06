import sys
import time
from datetime import datetime
from enum import Enum
from typing import List

from rich import markup
from rich.console import Console
from rich.table import Table

from sifflet.apis.client.model.rule_catalog_asset_dto import RuleCatalogAssetDto
from sifflet.apis.client.model.rule_overview_dto import RuleOverviewDto
from sifflet.apis.client.model.rule_run_dto import RuleRunDto
from sifflet.errors import exception_handler
from sifflet.logger import logger
from sifflet.rules.api import RulesApi
from sifflet.utils import show_table


class StatusError(Enum):
    FAILED = RuleCatalogAssetDto.allowed_values.get(("last_run_status",)).get("FAILED")
    TECHNICAL_ERROR = RuleCatalogAssetDto.allowed_values.get(("last_run_status",)).get("TECHNICAL_ERROR")


class StatusSuccess(Enum):
    SUCCESS = RuleCatalogAssetDto.allowed_values.get(("last_run_status",)).get("SUCCESS")


class StatusRunning(Enum):
    RUNNING = RuleCatalogAssetDto.allowed_values.get(("last_run_status",)).get("RUNNING")
    PENDING = RuleCatalogAssetDto.allowed_values.get(("last_run_status",)).get("PENDING")


class RulesService:
    def __init__(self, sifflet_config):
        self.api_rules = RulesApi(sifflet_config)
        self.console = Console()

    @exception_handler
    def show_rules(self, filter_name: str):
        """Display rules in a table"""
        rules, total_count = self.api_rules.fetch_rules(filter_name)

        if rules:
            rules_cleaned = [
                {
                    "id": rule.get("id"),
                    "name": markup.escape(rule.get("name")),
                    "datasource_type": rule.get("datasource_type"),
                    "dataset_name": rule.get("dataset_name"),
                    "platform": rule.get("source_platform"),
                    "last_run_status": self._format_status(rule.get("last_run_status", default="")),
                    "last_run": str(datetime.fromtimestamp(rule.get("last_run", default=0) / 1000)),
                }
                for rule in rules
            ]

            table = Table()
            table.add_column("ID", no_wrap=True)
            table.add_column("Name", no_wrap=True)
            table.add_column("Datasource Type")
            table.add_column("Dataset")
            table.add_column("Platform")
            table.add_column("Last run status", justify="right")
            table.add_column("Last run date")
            for val in rules_cleaned:
                table.add_row(*val.values())
            self.console.print(table)

            if len(rules) < int(total_count):
                self.console.print(f"Showing first {len(rules)} rules out of {total_count} rules")
        elif filter_name:
            logger.info(f"No rule found for search filter: [bold]{filter_name}[/]")
        else:
            logger.info("No rule found")

    @exception_handler
    def run_rules(self, rule_ids: List[str]) -> None:
        rule_runs: List[RuleRunDto] = []
        for rule_id in rule_ids:
            logger.info(f"Triggering rule {rule_id} ...")
            rule_run: RuleRunDto = self.api_rules.run_rule(rule_id)
            rule_runs.append(rule_run)

        rule_run_fail: List[RuleRunDto] = []
        rule_run_success: List[RuleRunDto] = []
        time.sleep(1)
        for rule_run in rule_runs:
            rule_run_fail, rule_run_success = self._get_status_rule_run(rule_run, rule_run_fail, rule_run_success)

        for rule_run in rule_run_success:
            logger.info(f"Rule success, id={rule_run}")

        for rule_run in rule_run_fail:
            logger.error(f"Rule failed, id = {rule_run.get('id')}, result = \"{rule_run.get('result')}\"")
        if len(rule_run_fail) >= 1:
            logger.error("One or many rules are on fail.")
            sys.exit(1)

    def _get_status_rule_run(self, rule_run: RuleRunDto, rule_run_fail, rule_run_success):
        rule_run_dto: RuleRunDto = self.api_rules.status_rule_run(rule_run.get("id"), rule_run.get("rule_id"))
        logger.debug(f"Rules status = {rule_run_dto.get('status')}")
        status = rule_run_dto.get("status")
        if status in StatusError.__members__:
            rule_run_fail.append(rule_run)
        elif status in StatusSuccess.__members__:
            rule_run_success.append(rule_run)
        else:
            rule_run_fail, rule_run_success = self._get_status_rule_run(rule_run, rule_run_fail, rule_run_success)
        return rule_run_fail, rule_run_success

    def show_run_history(self, rule_id: str):
        rule_overview: RuleOverviewDto = self.api_rules.overview_rule(rule_id=rule_id)

        rule_runs, total_count = self.api_rules.rule_runs(rule_id)
        if rule_runs:
            rules_runs_cleaned = [
                {
                    "status": self._format_status(rule_run.get("status", default="")),
                    "start_date": str(datetime.fromtimestamp(rule_run.get("start_date", default=0) / 1000)),
                    "end_date": str(datetime.fromtimestamp(rule_run.get("end_date", default=0) / 1000)),
                    "type": markup.escape(rule_run.get("type")),
                    "result": markup.escape(rule_run.get("result")),
                }
                for rule_run in rule_runs
            ]
            table_title = (
                f"Rule name: [{rule_overview.get('datasource_name')}]"
                f"[{rule_overview.get('dataset_name')}]{rule_overview.get('name')}"
            )
            show_table(rules_runs_cleaned, title=table_title)
            if len(rule_runs) < int(total_count):
                self.console.print(f"Showing first {len(rule_runs)} runs out of {total_count} runs")

    @staticmethod
    def _format_status(status: str) -> str:
        result = status
        if status in StatusError.__members__:
            result = f"[bold red]{status}[/bold red]"
        elif status in StatusSuccess.__members__:
            result = f"[bold green]{status}[/bold green]"

        return result
