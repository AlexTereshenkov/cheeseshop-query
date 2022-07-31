from typing import Optional, Callable

from packaging.version import Version

from cheeseshop.repository.package import Package, PackageFile
from cheeseshop.repository.types import Releases


def is_stable_version(version: Version) -> bool:
    """Check whether a version is in a stable version notation."""
    return not any(
        (
            version.is_devrelease,
            version.is_prerelease,
            version.is_postrelease,
        )
    )


def get_versions(
    releases: dict[Version, list[PackageFile]], filters: list[Callable]
) -> list[Optional[Version]]:
    """Get release versions applying filters."""
    return [
        version
        for version, url in releases.items()
        if all((f(version) for f in filters))
    ]


def filter_releases(
    package: Package,
    python_version: str,
    package_type: str,
    platform: str,
    arch: str,
) -> Releases:
    """Filter releases by querying the collection."""
    releases_matching_query = {}
    for version, package_files in package.releases.items():
        compatible_package_files = []
        for package_file in package_files:
            if (
                package_file.package_type.value == package_type
                and package_file.python_version == python_version
                and platform in package_file.filename
                and arch in package_file.filename
            ):
                compatible_package_files.append(package_file)
        if compatible_package_files:
            releases_matching_query[version] = compatible_package_files
    return releases_matching_query
