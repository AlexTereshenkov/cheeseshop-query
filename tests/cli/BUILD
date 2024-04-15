python_tests(
    name="tests",
    dependencies=[
        "cheeseshop:project-version",
        ":cassettes",
    ],
    extra_env_vars=["PEX_EXTRA_SYS_PATH"]
)

resources(
    name="cassettes",
    sources=["cassettes/*"],
)
