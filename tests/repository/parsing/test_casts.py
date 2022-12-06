import unittest
from unittest.mock import Mock

import dateutil
import pytest

from cheeseshop.repository.parsing.casts import (
    from_bool,
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    to_class,
    to_enum,
)
from cheeseshop.repository.parsing.exceptions import TypeErrorException


@pytest.mark.parametrize(
    "type_, value", [(unittest.mock.Mock, Mock(to_dict=Mock(side_effect=lambda: {})))]
)
def test_to_class(type_, value):
    assert to_class(c=type_, x=value) == {}
    with pytest.raises(TypeErrorException):
        to_class(c=int, x=value)


@pytest.mark.parametrize("type_, value", [(unittest.mock.Mock, Mock(value="value"))])
def test_to_enum(type_, value):
    assert to_enum(c=type_, x=value) == "value"
    with pytest.raises(TypeErrorException):
        to_enum(c=int, x=value)


@pytest.mark.parametrize("value", [42])
def test_from_int(value):
    assert from_int(x=value) == value
    for item in ["string", False]:
        with pytest.raises(TypeErrorException):
            from_int(x=item)


@pytest.mark.parametrize("value", ["string"])
def test_from_str(value):
    assert from_str(x=value) == value
    with pytest.raises(TypeErrorException):
        from_str(x=42)


@pytest.mark.parametrize("value", [None])
def test_from_none(value):
    assert from_none(x=value) is value
    with pytest.raises(TypeErrorException):
        from_none(x=42)


@pytest.mark.parametrize("value", [False])
def test_from_bool(value):
    assert from_bool(x=value) is value
    with pytest.raises(TypeErrorException):
        from_bool(x="string")


@pytest.mark.parametrize("value", ["2006-12-02T02:07:43"])
def test_from_datetime(value):
    assert from_datetime(x=value) == dateutil.parser.parse("2006-12-02T02:07:43")
    with pytest.raises(TypeErrorException):
        from_datetime(x=42)


@pytest.mark.parametrize("value", [["string1", "string2"]])
def test_from_list(value):
    with pytest.raises(TypeErrorException):
        from_list(f=lambda x: x, x=42)

    assert from_list(f=lambda item: item, x=value) == value
    mock = Mock(__name__="function", side_effect=TypeErrorException("string1", int))
    with pytest.raises(TypeErrorException) as err:
        from_list(f=mock, x=value)
    assert type(err.value) == TypeErrorException


@pytest.mark.parametrize("value", [{"key": "value"}])
def test_from_dict(value):
    with pytest.raises(TypeErrorException):
        from_dict(f=lambda x: x, x=42)

    assert from_dict(f=lambda item: item, x=value) == value
    mock = Mock(__name__="function", side_effect=TypeErrorException("string1", int))
    with pytest.raises(TypeErrorException) as err:
        from_dict(f=mock, x=value)
    assert type(err.value) == TypeErrorException


@pytest.mark.parametrize(
    "value, fs", [({"key": "value"}, [lambda item: item, lambda item: item])]
)
def test_from_union(value, fs):
    assert from_union(fs=fs, x=value) == value
    mock = Mock(__name__="function", side_effect=TypeErrorException("string1", int))
    with pytest.raises(TypeErrorException) as err:
        from_union(fs=[mock], x=value)
    assert type(err.value) == TypeErrorException
