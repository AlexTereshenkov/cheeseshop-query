class PackageNotFoundError(Exception):
    pass


class TypeErrorException(TypeError):
    """Unmet expectation for an object to be of a particular type."""

    def __init__(self, value, expected_type):
        message = (
            f"{value} is expected to be of {expected_type}, but is of {type(value)}"
        )
        super().__init__(message)
