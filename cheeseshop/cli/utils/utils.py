from collections.abc import Iterable

# forbidden import
# from cheeseshop.repository.parsing.casts import from_none


def choices(option_type: Iterable) -> list[str]:
    """Get click option choices from an iterable."""
    return [str(item.value) for item in option_type]
