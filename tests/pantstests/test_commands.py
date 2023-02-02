from pathlib import Path

import pytest


@pytest.mark.vcr()
def test_generate_test_data_with_pants_shell_command():
    """Test running a test that is known to cause generation of a file via a
    shell command."""
    package_name = (
        Path("tests/pantstests/testdata/test_package_name.txt").read_text().strip()
    )
    assert package_name == Path("tests/pantstests/package_name").read_text().strip()
