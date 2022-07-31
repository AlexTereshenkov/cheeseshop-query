from collections.abc import Iterable


def choices(option_type: Iterable) -> list[str]:
    """Get click option choices from an iterable."""
    return [str(item.value) for item in option_type]
