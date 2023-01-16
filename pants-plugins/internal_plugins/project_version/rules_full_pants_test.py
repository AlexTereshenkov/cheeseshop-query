import json
from pathlib import Path

from pants.testutil.pants_integration_test import run_pants, setup_tmpdir

build_root_marker = Path.cwd().joinpath("BUILDROOT")


def test_reading_project_version_target() -> None:
    """Run a full Pants process as it would run on the command line reading a
    `version_file` target."""
    project_files = {
        "project/BUILD": "version_file(source='VERSION')",
        "project/VERSION": "10.6.1",
    }
    build_root_marker.touch()
    with setup_tmpdir(project_files) as tmpdir:
        result = run_pants(
            [
                (
                    "--backend-packages="
                    "['pants.backend.python', 'internal_plugins.project_version']"
                ),
                "project-version",
                "--as-json",
                f"{tmpdir}/project:",
            ],
        )
        result.assert_success()
        assert result.stdout.strip() == json.dumps(
            {"path": f"{tmpdir}/project/VERSION", "version": "10.6.1"}
        )
    build_root_marker.unlink()
