from typing import List, Tuple

from sifflet.apis.base import BaseApi, DEFAULT_ITEMS_PER_PAGE, DEFAULT_PAGE_NUM
from sifflet.apis.client.api import sifflet_rule_api, sifflet_rule_run_api
from sifflet.apis.client.model.rule_catalog_asset_dto import RuleCatalogAssetDto
from sifflet.apis.client.model.rule_overview_dto import RuleOverviewDto
from sifflet.apis.client.model.rule_run_dto import RuleRunDto
from sifflet.apis.client.model.search_collection_rule_catalog_asset_dto import SearchCollectionRuleCatalogAssetDto
from sifflet.logger import logger


class RulesApi(BaseApi):
    def __init__(self, sifflet_config):
        super().__init__(sifflet_config)
        self.api_instance_rule = sifflet_rule_api.SiffletRuleApi(self.api)
        self.api_instance_rule_run = sifflet_rule_run_api.SiffletRuleRunApi(self.api)

    def fetch_rules(
        self, filter_: str, items_per_page=DEFAULT_ITEMS_PER_PAGE, page=DEFAULT_PAGE_NUM
    ) -> Tuple[List[RuleCatalogAssetDto], int]:
        """Get a list of rules for a given filter"""
        logger.debug(f"Fetch rules with search filter = {filter_}")
        if not filter_:
            filter_ = ""
        response: SearchCollectionRuleCatalogAssetDto = self.api_instance_rule.get_all_rule(
            items_per_page=items_per_page,
            page=page,
            text_search=filter_,
            sort=[RuleCatalogAssetDto.attribute_map["name"] + ",ASC"],
        )
        return response.get("data"), response.get("total_elements")

    def run_rule(self, id_: str) -> RuleRunDto:
        """Run a rule and return the runRunId of the created run"""
        logger.debug(f"Run rule_id = {id_}")
        # TODO: backend should check if the rule is already running, and throw an exception if running
        return self.api_instance_rule.sifflet_rule_manual_run(id=id_)

    def status_rule_run(self, run_id: str, rule_id: str) -> RuleRunDto:
        """Get details of a RuleRun"""
        logger.debug(f"Fetch rule run, id = {run_id} of rule {rule_id}")
        return self.api_instance_rule_run.get_sifflet_rule_run(id=rule_id, run_id=run_id)

    def overview_rule(self, rule_id: str) -> RuleOverviewDto:
        """Get details of a Rule"""
        logger.debug(f"Fetch rule, id = {rule_id}")
        return self.api_instance_rule.get_sifflet_rule_overview(id=rule_id)

    def rule_runs(
        self, id_: str, items_per_page=DEFAULT_ITEMS_PER_PAGE, page=DEFAULT_PAGE_NUM
    ) -> Tuple[List[RuleRunDto], int]:
        """Get a list of RuleRun for a given ruleId"""
        logger.debug(f"Fetch rule run, rule_id = {id_}")
        response = self.api_instance_rule_run.get_sifflet_rule_runs(
            id=id_,
            items_per_page=items_per_page,
            page=page,
            sort=[RuleRunDto.attribute_map["start_date"] + ",DESC"],
        )
        return response.get("data"), response.get("total_elements")
