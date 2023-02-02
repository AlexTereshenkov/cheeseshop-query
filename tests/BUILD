experimental_shell_command(
    name="shell-script-to-prepare-test-data",
    command="./write_test_package_name.sh",
    tools=["echo", "bash"],
    dependencies=[":shell-scripts"],
    outputs=["testdata/"],
    log_output=True,
)

shell_sources(name="shell-scripts", sources=["write_test_package_name.sh"])
