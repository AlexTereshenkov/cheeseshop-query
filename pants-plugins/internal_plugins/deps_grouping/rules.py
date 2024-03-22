import json
import logging
from dataclasses import dataclass

from pants.backend.python.target_types import PythonDependenciesField
from pants.engine.addresses import Addresses, UnparsedAddressInputs


logger = logging.getLogger(__name__)

from pants.build_graph.address import Address
from pants.engine.fs import DigestContents
from pants.engine.internals.native_engine import Digest
from pants.engine.internals.selectors import Get
from pants.engine.rules import collect_rules, rule
from pants.engine.target import (
    FieldSet,
    HydratedSources,
    HydrateSourcesRequest,
    InferDependenciesRequest,
    InferredDependencies,
    Targets,
)
from pants.engine.unions import UnionRule

from internal_plugins.deps_grouping.target_types import (
    DepsGroupSourceField,
    DepsGroupTarget,
)


@dataclass(frozen=True)
class DepsGroupsFileView:
    path: str
    contents: str


@dataclass(frozen=True)
class DepsGroupDependencyInferenceFieldSet(FieldSet):
    required_fields = (DepsGroupSourceField,)

    source: DepsGroupSourceField


class InferDepsGroupDependenciesRequest(InferDependenciesRequest):
    infer_from = DepsGroupDependencyInferenceFieldSet


@rule("Get dependencies of a deps_group target.")
async def extend_dependencies(
    request: InferDepsGroupDependenciesRequest,
) -> InferredDependencies:
    """This rule is used when running `pants dependencies //:deps-group-1`."""
    sources = await Get(
        HydratedSources, HydrateSourcesRequest(request.field_set.source)
    )
    digest_contents = await Get(DigestContents, Digest, sources.snapshot.digest)
    file_content = digest_contents[0]
    requirements = json.loads(file_content.content.decode("utf-8").strip())

    addresses = []
    for req in requirements[request.field_set.address.target_name]:
        addresses.append(
            Address("requirements", target_name="requirements", generated_name=req),
        )

    return InferredDependencies(addresses)


@dataclass
class RequirementsAddresses:
    """List of addresses to python_requirement targets."""

    addresses: list[Address]


@rule("Read requirements from JSON file.")
async def read_deps_group_target_requirements_from_json_file(
    target: DepsGroupTarget,
) -> RequirementsAddresses:
    """This rule is used to get requirements of a given `deps_group` target
    from a JSON file."""
    sources = await Get(
        HydratedSources, HydrateSourcesRequest(target.get(DepsGroupSourceField))
    )
    digest_contents = await Get(DigestContents, Digest, sources.snapshot.digest)
    file_content = digest_contents[0]
    requirements = json.loads(file_content.content.decode("utf-8").strip())

    addresses = []
    for req in requirements[target.address.target_name]:
        addresses.append(
            Address("requirements", target_name="requirements", generated_name=req),
        )
    return RequirementsAddresses(addresses=addresses)


@dataclass(frozen=True)
class PythonSourcesExtensionFieldSet(FieldSet):
    """Extension of python sources field set to be used in a custom dependency
    inference request."""

    required_fields = (PythonDependenciesField,)
    dependencies: PythonDependenciesField


class PythonSourcesExtensionInferDependenciesRequest(InferDependenciesRequest):
    infer_from = PythonSourcesExtensionFieldSet


@rule(
    "Get Python requirements that a Python source module depends on via a dependency group."
)
async def get_dep_group_dependencies_python_sources(
    request: PythonSourcesExtensionInferDependenciesRequest,
) -> InferredDependencies:
    all_requirements_addresses = []
    for dep_string in request.field_set.dependencies.value:
        targets = await Get(
            Targets,
            UnparsedAddressInputs(
                [dep_string],
                owning_address=None,
                description_of_origin="pants-plugins",
            ),
        )
        for target in targets:
            requirements = await Get(RequirementsAddresses, DepsGroupTarget, target)
            for req in requirements.addresses:
                all_requirements_addresses.append(req)

    return InferredDependencies(Addresses(all_requirements_addresses))


def rules():
    return (
        *collect_rules(),
        UnionRule(InferDependenciesRequest, InferDepsGroupDependenciesRequest),
        UnionRule(
            InferDependenciesRequest, PythonSourcesExtensionInferDependenciesRequest
        ),
    )
