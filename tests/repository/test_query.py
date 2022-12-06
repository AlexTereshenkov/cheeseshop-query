import pytest
from packaging.version import Version

from cheeseshop.repository.package import Package, PackageFile
from cheeseshop.repository.properties import PackageType
from cheeseshop.repository.query import filter_releases, get_versions, is_stable_version


@pytest.mark.parametrize(
    "version, expected",
    (
        (Version("1.2.3"), True),
        (Version("1.2.3rc4"), False),
        (Version("1.2.3.dev4"), False),
        (Version("1.2.3.post4"), False),
    ),
)
def test_is_stable_version(version, expected):
    assert is_stable_version(version) == expected


@pytest.mark.parametrize(
    "releases, filters, expected",
    (
        ({Version("9"): [], Version("7"): []}, [lambda v: v > Version("10")], []),
        (
            {Version("9"): [], Version("7"): []},
            [lambda v: v > Version("8")],
            [Version("9")],
        ),
        (
            {Version("9"): [], Version("11"): []},
            [lambda v: v > Version("8"), lambda v: v < Version("10")],
            [Version("9")],
        ),
    ),
)
def test_get_versions(releases, filters, expected):
    assert get_versions(releases, filters) == expected


@pytest.mark.parametrize(
    "package, python_version, package_type, platform, arch, expected",
    (
        (
            Package(
                releases={
                    Version("1.2.3"): [
                        PackageFile(
                            package_type=PackageType.BDIST_WHEEL,
                            filename="package-1.2.3-cp38-cp38-macosx_10_9_x86_64.whl",
                            python_version="cp38",
                        ),
                    ],
                    Version("1.2.4"): [
                        PackageFile(
                            package_type=PackageType.SDIST,
                            filename="package-1.2.4.tar.gz",
                            python_version="source",
                        ),
                    ],
                    Version("1.2.5"): [
                        PackageFile(
                            package_type=PackageType.BDIST_WHEEL,
                            filename="package-1.2.4-cp310-cp310-macosx_11_0_arm64.whl",
                            python_version="cp310",
                        ),
                    ],
                }
            ),
            "cp38",
            "bdist_wheel",
            "macos",
            "x86_64",
            {
                Version("1.2.3"): [
                    PackageFile(
                        package_type=PackageType.BDIST_WHEEL,
                        filename="package-1.2.3-cp38-cp38-macosx_10_9_x86_64.whl",
                        python_version="cp38",
                    ),
                ],
            },
        ),
    ),
)
def test_filter_releases(
    package, python_version, package_type, platform, arch, expected
):
    assert (
        filter_releases(
            package=package,
            python_version=python_version,
            package_type=package_type,
            platform=platform,
            arch=arch,
        )
        == expected
    )
