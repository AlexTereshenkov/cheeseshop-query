from experiment.targets import ProjectVersionTarget
import experiment.custom_rules as custom_rules


def target_types():
    return [ProjectVersionTarget]


def rules():
    return [*custom_rules.rules()]
