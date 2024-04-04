python_tests(
    name="tests",
    dependencies=[
        "cheeseshop:project-version",
        ":cassettes",
    ],
    environment=parametrize(
        "docker_debian_3_9",
        "docker_debian_3_10",
        "docker_debian_3_11",
        "docker_debian_3_12",
    ),
)

resources(
    name="cassettes",
    sources=["cassettes/*"],
)
