import pkgutil

VERSION: str = pkgutil.get_data(__name__, "VERSION").decode().strip()
