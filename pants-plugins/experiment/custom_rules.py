from pants.engine.console import Console
from pants.engine.goal import GoalSubsystem, Goal
from pants.engine.internals.selectors import Get
from pants.engine.rules import collect_rules, rule, goal_rule
from pants.engine.target import Targets

from experiment.targets import CustomTarget, CustomField
from dataclasses import dataclass


import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MyResult:
    result: str


@rule
async def read_target_fields(custom_target: CustomTarget) -> MyResult:
    logger.info(f"Accessing <custom_target.alias>: {custom_target.alias}")
    logger.info(f"Accessing <custom_target.custom_field>: {custom_target[CustomField]}")
    # TODO: how to set value for a field?
    # #custom_target[CustomField].value = "SomeValue"
    return MyResult(result=custom_target[CustomField].value)


class HelloWorldSubsystem(GoalSubsystem):
    name = "hello-world"
    help = "An example goal."


class HelloWorld(Goal):
    subsystem_cls = HelloWorldSubsystem


@goal_rule
async def main(console: Console, targets: Targets) -> HelloWorld:
    targets = [tgt for tgt in targets if tgt.has_field(CustomField)]
    for target in targets:
        console.print_stdout(target.address.spec)
        result = await Get(MyResult, CustomTarget, target)
        console.print_stdout(result)
    return HelloWorld(exit_code=0)


def rules():
    return collect_rules()
