from typing import List

import click
from click_aliases import ClickAliasedGroup

from sifflet.constants import SIFFLET_CONFIG_CTX
from sifflet.rules.service import RulesService


@click.group(cls=ClickAliasedGroup)
def rules():
    """List and control rules"""


@rules.command(name="list", aliases=["ls"])
@click.option("--name", "-n", "text", type=str, required=False, help="Search rules by name")
@click.pass_context
def list_rules(ctx, text: str):
    """Display all rules created"""
    sifflet_config = ctx.obj[SIFFLET_CONFIG_CTX]
    service = RulesService(sifflet_config)
    service.show_rules(text)


@rules.command()
@click.option("--id", "ids", multiple=True, required=True, help="The rule id to trigger")
@click.pass_context
def run(ctx, ids: List[str]):
    """Run one or many rules by its id(s)"""
    sifflet_config = ctx.obj[SIFFLET_CONFIG_CTX]
    service = RulesService(sifflet_config)
    service.run_rules(ids)


@rules.command("run_history")
@click.option("--id", "rule_id", required=True, help="id of the rules id to fetch")
@click.pass_context
def run_history(ctx, rule_id: str):
    """Display all rule runs for a given rule_id"""
    sifflet_config = ctx.obj[SIFFLET_CONFIG_CTX]
    service = RulesService(sifflet_config)
    service.show_run_history(rule_id=rule_id)
