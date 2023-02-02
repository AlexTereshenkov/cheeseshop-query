python_tests(
    name="tests",
    dependencies=[":shell-script-to-prepare-test-data", ":package-name-file"],
)

experimental_shell_command(
    name="shell-script-to-prepare-test-data",
    command="./write_test_package_name.sh",
    tools=["echo", "bash"],
    dependencies=[":shell-scripts"],
    outputs=["testdata/"],
    log_output=True,
)

shell_sources(name="shell-scripts", sources=["write_test_package_name.sh"])

resource(name="package-name-file", source="package_name")
