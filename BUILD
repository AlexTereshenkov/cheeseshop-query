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
        #"cheeseshop:project-version",
        "cheeseshop/cli:cheeseshop-query",
    ],
    provides=python_artifact(
        name="cheeseshop-query",
    ),
    sdist=False,
    generate_setup=False,
)
