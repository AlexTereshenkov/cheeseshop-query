from cheeseshop.version import VERSION
from setuptools import setup, find_packages

setup(
    name="cheeseshop-query",
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points={
        "console_scripts": [
            f"cheeseshop-query = cheeseshop.cli.cli:cli",
        ],
    },
    include_package_data=True,
    version=VERSION,
    install_requires=["click"],
)
