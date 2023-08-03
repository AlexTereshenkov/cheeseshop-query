python_tests(
    name="tests",
    dependencies=[":shell-script-to-prepare-test-data", ":package-name-file"],
)

shell_command(
    name="shell-script-to-prepare-test-data",
    command="./write_test_package_name.sh",
    tools=["echo", "bash", "mkdir"],
    execution_dependencies=[":shell-scripts"],
    output_directories=["testdata/"],
    log_output=True,
)

shell_sources(
    name="shell-scripts",
    sources=["write_test_package_name.sh"],
)

resource(
    name="package-name-file",
    source="package_name",
)
