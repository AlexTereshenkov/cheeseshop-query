python_sources(
    name="root",
)

python_sources(
    name="setup-py",
    sources=["setup.py"],
)

resource(
    name="MANIFEST",
    source="MANIFEST.in",
)

python_distribution(
    name="cheeseshop-query-wheel",
    dependencies=[
        ":setup-py",
        ":MANIFEST",
        "cheeseshop:project-version",
        "cheeseshop/cli:cheeseshop-query",
    ],
    provides=python_artifact(
        name="cheeseshop-query",
    ),
    sdist=False,
    generate_setup=False,
)

docker_environment(
    name="docker_debian_3_9",
    platform="linux_x86_64",
    image="python:3.9.19-slim-bookworm@sha256:0b4b0801ae9ae61bb57bc738b1efbe4e16b927fd581774c8edfed90f0e0f01ad",
    python_bootstrap_search_path=["/usr/local/bin"],
)

docker_environment(
    name="docker_debian_3_10",
    platform="linux_x86_64",
    image="python:3.10.14-slim-bookworm@sha256:0b4b0801ae9ae61bb57bc738b1efbe4e16b927fd581774c8edfed90f0e0f01ad",
    python_bootstrap_search_path=["/usr/local/bin"],
)

docker_environment(
    name="docker_debian_3_11",
    platform="linux_x86_64",
    image="python:3.11.8-slim-bookworm@sha256:90f8795536170fd08236d2ceb74fe7065dbf74f738d8b84bfbf263656654dc9b",
    python_bootstrap_search_path=["/usr/local/bin"],
)


docker_environment(
    name="docker_debian_3_12",
    platform="linux_x86_64",
    image="python:3.12.2-slim-bookworm@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997",
    python_bootstrap_search_path=["/usr/local/bin"],
)
