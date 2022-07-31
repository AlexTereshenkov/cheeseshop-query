from enum import Enum


class Architecture(Enum):
    X86_64 = "x86_64"
    ARM = "arm64"


class Platform(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"


class PackageType(Enum):
    BDIST_WHEEL = "bdist_wheel"
    BDIST_EGG = "bdist_egg"
    BDIST_WININST = "bdist_wininst"
    BDIST_DUMB = "bdist_dumb"
    SDIST = "sdist"


# packaging package specification?
# requirement specification marker

# class RequiresPython(Enum):
#     THE_2730313233 = ">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*"
#     THE_35 = ">=3.5"
#     THE_36 = ">=3.6"
#     THE_37 = ">=3.7"
#     THE_37311 = ">=3.7,<3.11"
#     THE_38 = ">=3.8"
