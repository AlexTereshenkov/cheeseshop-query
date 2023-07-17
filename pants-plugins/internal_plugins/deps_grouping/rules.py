import json
from dataclasses import dataclass

import logging

from pants.backend.python.dependency_inference.rules import InferPythonImportDependencies, \
    PythonImportDependenciesInferenceFieldSet
from pants.backend.python.target_types import PythonDependenciesField
from pants.engine.addresses import Addresses, UnparsedAddressInputs
from pants.util.ordered_set import FrozenOrderedSet

logger = logging.getLogger(__name__)

from pants.build_graph.address import Address
from pants.engine.fs import DigestContents
from pants.engine.internals.native_engine import Digest
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.rules import collect_rules, rule
from pants.engine.target import (
    FieldSet,
    HydratedSources,
    HydrateSourcesRequest,
    InferDependenciesRequest,
    InferredDependencies, Targets, DependenciesRequest, Dependencies,
)
from pants.engine.unions import UnionRule

from internal_plugins.deps_grouping.target_types import (
    DepsGroupSourceField,
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


@rule
async def extend_dependencies(
    request: InferDepsGroupDependenciesRequest,
) -> InferredDependencies:
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


class MyDependencies(Dependencies):
    pass


@dataclass(frozen=True)
class MyFieldSet(FieldSet):
    required_fields = (
        PythonDependenciesField,
    )
    dependencies: PythonDependenciesField


class MyInferDependenciesRequest(InferDependenciesRequest):
    infer_from = MyFieldSet


@rule
async def get_dependencies_python_sources(
    request: MyInferDependenciesRequest,
) -> InferredDependencies:
    # logger.info(request.field_set.dependencies)
    for dep_string in request.field_set.dependencies.value:
        targets = await Get(Targets, UnparsedAddressInputs([dep_string], owning_address=None, description_of_origin="me"))
        for target in targets:
            logger.info(target)
            logger.info(type(target))
            # this doesn't work - the matching rule can't be found
            # deps = await Get(Addresses, InferDepsGroupDependenciesRequest(target.get(Dependencies)))
            # logger.info(deps)

    return InferredDependencies([])


def rules():
    return (
        *collect_rules(),
        UnionRule(InferDependenciesRequest, InferDepsGroupDependenciesRequest),
        UnionRule(InferDependenciesRequest, MyInferDependenciesRequest),
    )
