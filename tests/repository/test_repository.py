from unittest.mock import Mock, patch

import pytest

from cheeseshop.repository.parsing.exceptions import PackageNotFoundError
from cheeseshop.repository.repository import Repository


@pytest.mark.vcr()
def test_get_repository_package(caplog):
    repo = Repository()
    package = repo.get("packaging")
    assert package.to_dict()
    assert package.info.to_dict()
    assert package.urls[0].to_dict()

    with patch(
        "cheeseshop.repository.repository.requests.get",
        lambda *args, **kwargs: Mock(status_code=404, reason="Not found"),
    ):
        with pytest.raises(SystemExit):
            repo.get("packaging")

    with patch(
        "cheeseshop.repository.repository.requests.get",
        lambda *args, **kwargs: Mock(
            name="requests.Response", status_code=200, text='{"message": "not found"}'
        ),
    ):
        with pytest.raises(PackageNotFoundError):
            repo.get("packaging")
