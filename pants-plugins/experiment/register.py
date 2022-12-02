from experiment.targets import CustomTarget
import experiment.custom_rules as custom_rules


def target_types():
    return [CustomTarget]


def rules():
    return [*custom_rules.rules()]
