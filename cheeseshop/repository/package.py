import reprlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from packaging.version import Version
from typing_extensions import TypeAlias

from cheeseshop.repository.parsing.casts import (
    from_bool,
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
    to_enum,
)
from cheeseshop.repository.properties import PackageType

# forbidden import
# from cheeseshop.cli.utils.utils import choices


@dataclass
class Downloads:
    last_day: Optional[int] = None
    last_month: Optional[int] = None
    last_week: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Downloads":
        assert isinstance(obj, dict)
        last_day = from_union([from_int, from_none], obj.get("last_day"))
        last_month = from_union([from_int, from_none], obj.get("last_month"))
        last_week = from_union([from_int, from_none], obj.get("last_week"))
        return Downloads(last_day, last_month, last_week)

    def to_dict(self) -> dict:
        result: dict = {}
        result["last_day"] = from_union([from_int, from_none], self.last_day)
        result["last_month"] = from_union([from_int, from_none], self.last_month)
        result["last_week"] = from_union([from_int, from_none], self.last_week)
        return result


@dataclass
class ProjectUrls:
    bug_tracker: Optional[str] = None
    documentation: Optional[str] = None
    download: Optional[str] = None
    homepage: Optional[str] = None
    source_code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "ProjectUrls":
        assert isinstance(obj, dict)
        bug_tracker = from_union([from_str, from_none], obj.get("Bug Tracker"))
        documentation = from_union([from_str, from_none], obj.get("Documentation"))
        download = from_union([from_str, from_none], obj.get("Download"))
        homepage = from_union([from_str, from_none], obj.get("Homepage"))
        source_code = from_union([from_str, from_none], obj.get("Source Code"))
        return ProjectUrls(bug_tracker, documentation, download, homepage, source_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Bug Tracker"] = from_union([from_str, from_none], self.bug_tracker)
        result["Documentation"] = from_union([from_str, from_none], self.documentation)
        result["Download"] = from_union([from_str, from_none], self.download)
        result["Homepage"] = from_union([from_str, from_none], self.homepage)
        result["Source Code"] = from_union([from_str, from_none], self.source_code)
        return result


@dataclass
class Info:
    bugtrack_url: Optional[str] = None
    docs_url: Optional[str] = None
    requires_dist: Optional[list] = None
    yanked_reason: Optional[str] = None
    author: Optional[str] = None
    author_email: Optional[str] = None
    classifiers: Optional[List[str]] = None
    description: Optional[str] = None
    description_content_type: Optional[str] = None
    download_url: Optional[str] = None
    downloads: Optional[Downloads] = None
    home_page: Optional[str] = None
    keywords: Optional[str] = None
    license: Optional[str] = None
    maintainer: Optional[str] = None
    maintainer_email: Optional[str] = None
    name: Optional[str] = None
    package_url: Optional[str] = None
    platform: Optional[str] = None
    project_url: Optional[str] = None
    project_urls: Optional[ProjectUrls] = None
    release_url: Optional[str] = None
    # TODO(alte): requires_python: Optional[RequiresPython] = None
    requires_python: Optional[str] = None
    summary: Optional[str] = None
    version: Optional[str] = None
    yanked: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "Info":
        assert isinstance(obj, dict)
        bugtrack_url = from_union([from_str, from_none], obj.get("bugtrack_url"))
        docs_url = from_union([from_str, from_none], obj.get("docs_url"))
        requires_dist = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("requires_dist")
        )
        yanked_reason = from_union([from_str, from_none], obj.get("yanked_reason"))
        author = from_union([from_str, from_none], obj.get("author"))
        author_email = from_union([from_str, from_none], obj.get("author_email"))
        classifiers = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("classifiers")
        )
        description = from_union([from_str, from_none], obj.get("description"))
        description_content_type = from_union(
            [from_str, from_none], obj.get("description_content_type")
        )
        download_url = from_union([from_str, from_none], obj.get("download_url"))
        downloads = from_union([Downloads.from_dict, from_none], obj.get("downloads"))
        home_page = from_union([from_str, from_none], obj.get("home_page"))
        keywords = from_union([from_str, from_none], obj.get("keywords"))
        license = from_union([from_str, from_none], obj.get("license"))
        maintainer = from_union([from_str, from_none], obj.get("maintainer"))
        maintainer_email = from_union(
            [from_str, from_none], obj.get("maintainer_email")
        )
        name = from_union([from_str, from_none], obj.get("name"))
        package_url = from_union([from_str, from_none], obj.get("package_url"))
        platform = from_union([from_str, from_none], obj.get("platform"))
        project_url = from_union([from_str, from_none], obj.get("project_url"))
        project_urls = from_union(
            [ProjectUrls.from_dict, from_none], obj.get("project_urls")
        )
        release_url = from_union([from_str, from_none], obj.get("release_url"))
        requires_python = from_union([from_str, from_none], obj.get("requires_python"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        version = from_union([from_str, from_none], obj.get("version"))
        yanked = from_union([from_bool, from_none], obj.get("yanked"))
        return Info(
            bugtrack_url,
            docs_url,
            requires_dist,
            yanked_reason,
            author,
            author_email,
            classifiers,
            description,
            description_content_type,
            download_url,
            downloads,
            home_page,
            keywords,
            license,
            maintainer,
            maintainer_email,
            name,
            package_url,
            platform,
            project_url,
            project_urls,
            release_url,
            requires_python,
            summary,
            version,
            yanked,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["bugtrack_url"] = from_none(self.bugtrack_url)
        result["docs_url"] = from_none(self.docs_url)
        result["requires_dist"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.requires_dist
        )
        result["yanked_reason"] = from_union([from_str, from_none], self.yanked_reason)
        result["author"] = from_union([from_str, from_none], self.author)
        result["author_email"] = from_union([from_str, from_none], self.author_email)
        result["classifiers"] = from_union(
            # must be from_str
            [lambda x: from_list(from_str, x), from_none],
            self.classifiers,
        )
        result["description"] = from_union([from_str, from_none], self.description)
        result["description_content_type"] = from_union(
            [from_str, from_none], self.description_content_type
        )
        result["download_url"] = from_union([from_str, from_none], self.download_url)
        result["downloads"] = from_union(
            [lambda x: to_class(Downloads, x), from_none], self.downloads
        )
        result["home_page"] = from_union([from_str, from_none], self.home_page)
        result["keywords"] = from_union([from_str, from_none], self.keywords)
        result["license"] = from_union([from_str, from_none], self.license)
        result["maintainer"] = from_union([from_str, from_none], self.maintainer)
        result["maintainer_email"] = from_union(
            [from_str, from_none], self.maintainer_email
        )
        result["name"] = from_union([from_str, from_none], self.name)
        result["package_url"] = from_union([from_str, from_none], self.package_url)
        result["platform"] = from_union([from_str, from_none], self.platform)
        result["project_url"] = from_union([from_str, from_none], self.project_url)
        result["project_urls"] = from_union(
            [lambda x: to_class(ProjectUrls, x), from_none], self.project_urls
        )
        result["release_url"] = from_union([from_str, from_none], self.release_url)
        result["requires_python"] = from_union(
            [from_str, from_none], self.requires_python
        )
        result["summary"] = from_union([from_str, from_none], self.summary)
        result["version"] = from_union([from_str, from_none], self.version)
        result["yanked"] = from_union([from_bool, from_none], self.yanked)
        return result

    def __repr__(self):
        return reprlib.repr(self)


@dataclass
class Digests:
    md5: Optional[str] = None
    sha256: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Digests":
        assert isinstance(obj, dict)
        md5 = from_union([from_str, from_none], obj.get("md5"))
        sha256 = from_union([from_str, from_none], obj.get("sha256"))
        return Digests(md5, sha256)

    def to_dict(self) -> dict:
        result: dict = {}
        result["md5"] = from_union([from_str, from_none], self.md5)
        result["sha256"] = from_union([from_str, from_none], self.sha256)
        return result

    def __repr__(self):
        return reprlib.repr(self)


@dataclass
class PackageFile:
    yanked_reason: Optional[str] = None
    comment_text: Optional[str] = None
    digests: Optional[Digests] = None
    downloads: Optional[int] = None
    filename: Optional[str] = None
    has_sig: Optional[bool] = None
    md5_digest: Optional[str] = None
    package_type: Optional[PackageType] = None
    python_version: Optional[str] = None
    requires_python: Optional[str] = None
    size: Optional[int] = None
    upload_time: Optional[datetime] = None
    upload_time_iso_8601: Optional[datetime] = None
    url: Optional[str] = None
    yanked: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "PackageFile":
        assert isinstance(obj, dict)
        yanked_reason = from_union([from_str, from_none], obj.get("yanked_reason"))
        comment_text = from_union([from_str, from_none], obj.get("comment_text"))
        digests = from_union([Digests.from_dict, from_none], obj.get("digests"))
        downloads = from_union([from_int, from_none], obj.get("downloads"))
        filename = from_union([from_str, from_none], obj.get("filename"))
        has_sig = from_union([from_bool, from_none], obj.get("has_sig"))
        md5_digest = from_union([from_str, from_none], obj.get("md5_digest"))
        package_type = from_union([PackageType, from_none], obj.get("packagetype"))
        python_version = from_union([from_str, from_none], obj.get("python_version"))
        requires_python = from_union([from_str, from_none], obj.get("requires_python"))
        size = from_union([from_int, from_none], obj.get("size"))
        upload_time = from_union([from_datetime, from_none], obj.get("upload_time"))
        upload_time_iso_8601 = from_union(
            [from_datetime, from_none], obj.get("upload_time_iso_8601")
        )
        url = from_union([from_str, from_none], obj.get("url"))
        yanked = from_union([from_bool, from_none], obj.get("yanked"))
        return PackageFile(
            yanked_reason,
            comment_text,
            digests,
            downloads,
            filename,
            has_sig,
            md5_digest,
            package_type,
            python_version,
            requires_python,
            size,
            upload_time,
            upload_time_iso_8601,
            url,
            yanked,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["yanked_reason"] = from_union([from_str, from_none], self.yanked_reason)
        result["comment_text"] = from_union([from_str, from_none], self.comment_text)
        result["digests"] = from_union(
            [lambda x: to_class(Digests, x), from_none], self.digests
        )
        result["downloads"] = from_union([from_int, from_none], self.downloads)
        result["filename"] = from_union([from_str, from_none], self.filename)
        result["has_sig"] = from_union([from_bool, from_none], self.has_sig)
        result["md5_digest"] = from_union([from_str, from_none], self.md5_digest)
        result["package_type"] = from_union(
            [lambda x: to_enum(PackageType, x), from_none], self.package_type
        )
        result["python_version"] = from_union(
            [from_str, from_none], self.python_version
        )
        result["requires_python"] = from_union(
            [from_str, from_none], self.requires_python
        )
        result["size"] = from_union([from_int, from_none], self.size)
        result["upload_time"] = from_union(
            [lambda x: x.isoformat(), from_none], self.upload_time
        )
        result["upload_time_iso_8601"] = from_union(
            [lambda x: x.isoformat(), from_none], self.upload_time_iso_8601
        )
        result["url"] = from_union([from_str, from_none], self.url)
        result["yanked"] = from_union([from_bool, from_none], self.yanked)
        return result

    def __repr__(self):
        return reprlib.repr(self)


Releases: TypeAlias = dict[Version, list[PackageFile]]


@dataclass
class Package:
    info: Optional[Info] = None
    last_serial: Optional[int] = None
    releases: Optional[Releases] = None
    urls: Optional[List[PackageFile]] = None
    vulnerabilities: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Package":
        assert isinstance(obj, dict)
        info = from_union([Info.from_dict, from_none], obj.get("info"))
        last_serial = from_union([from_int, from_none], obj.get("last_serial"))
        releases = from_union(
            [
                lambda x: from_dict(lambda x: from_list(PackageFile.from_dict, x), x),
                from_none,
            ],
            {
                Version(version): release
                for version, release in obj.get("releases", {}).items()
            },
        )
        urls = from_union(
            [lambda x: from_list(PackageFile.from_dict, x), from_none], obj.get("urls")
        )
        vulnerabilities = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("vulnerabilities")
        )
        return Package(info, last_serial, releases, urls, vulnerabilities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["info"] = from_union([lambda x: to_class(Info, x), from_none], self.info)
        result["last_serial"] = from_union([from_int, from_none], self.last_serial)
        result["releases"] = from_union(
            [
                lambda x: from_dict(
                    lambda x: from_list(lambda x: to_class(PackageFile, x), x), x
                ),
                from_none,
            ],
            self.releases,
        )
        result["urls"] = from_union(
            [lambda x: from_list(lambda x: to_class(PackageFile, x), x), from_none],
            self.urls,
        )
        result["vulnerabilities"] = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], self.vulnerabilities
        )
        return result

    def __repr__(self):
        return reprlib.repr(self)
