import json
import sys
from typing import Optional

from loguru import logger
import requests

from cheeseshop.configs import DEFAULT_PYPI_REPOSITORY
from cheeseshop.repository.parsing.exceptions import PackageNotFoundError
from cheeseshop.repository.package import Package


class Repository:
    def __init__(self, url: Optional[str] = None):
        self.url = url if url else DEFAULT_PYPI_REPOSITORY

    def get(self, package_name: str) -> Package:
        """Search for a package."""
        url = f"{self.url}/pypi/{package_name}/json"
        logger.info(f"Querying {url}")
        response = requests.get(
            url=url,
            headers={"Content-Type": "text/plain"},
        )
        if response.status_code != requests.codes.OK:
            logger.error(f"{str(response.reason)}: {url}")
            sys.exit(1)

        result = json.loads(response.text)
        message = result.get("message", "")
        if message.lower() == "not found":
            raise PackageNotFoundError(
                f"Package `{package_name}` is not found at `{self.url}`"
            )

        package = Package.from_dict(result)
        return package
