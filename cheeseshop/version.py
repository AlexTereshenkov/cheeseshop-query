import pkgutil

import tabulate

VERSION: str = (
    pkgutil.get_data(__name__, "VERSION").decode().strip()  # type: ignore[union-attr]
)
