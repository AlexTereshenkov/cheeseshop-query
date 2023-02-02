from pathlib import Path


def test_generate_test_data_with_pants_shell_command():
    """Test running a test that is known to cause generation of a file.

    The file is generated via a shell command, see
    https://www.pantsbuild.org/docs/run-shell-commands.
    """
    package_name = (
        Path("tests/pantstests/testdata/test_package_name.txt").read_text().strip()
    )
    assert package_name == Path("tests/pantstests/package_name").read_text().strip()
