from setuptools import find_packages, setup

from cheeseshop.version import VERSION

setup(
    name="cheeseshop-query",
    packages=find_packages(exclude=["tests", "tests.*"]),
    entry_points={
        "console_scripts": [
            "cheeseshop-query = cheeseshop.cli.cli:cli",
        ],
    },
    include_package_data=True,
    version=VERSION,
    install_requires=["click", "loguru", "python-dateutil", "requests"],
)
