from datetime import datetime
from enum import Enum
from textwrap import shorten
from typing import Any, Callable, Dict, List, Type, TypeVar, cast

import dateutil.parser
from loguru import logger

from cheeseshop.repository.parsing.exceptions import TypeErrorException

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def to_class(c: Type[T], x: Any) -> dict:
    if not isinstance(x, c):
        raise TypeErrorException(value=x, expected_type=c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    if not isinstance(x, c):
        raise TypeErrorException(value=x, expected_type=c)
    return x.value


def from_int(x: Any) -> int:
    if not (isinstance(x, int) and not isinstance(x, bool)):
        raise TypeErrorException(value=x, expected_type=int)
    return x


def from_str(x: Any) -> str:
    if not isinstance(x, str):
        raise TypeErrorException(value=x, expected_type=str)
    return x


def from_none(x: Any) -> Any:
    if x is not None:
        raise TypeErrorException(value=x, expected_type=None)
    return x


def from_bool(x: Any) -> bool:
    if not isinstance(x, bool):
        raise TypeErrorException(value=x, expected_type=bool)
    return x


def from_datetime(x: Any) -> datetime:
    if not isinstance(x, str):
        raise TypeErrorException(value=x, expected_type=str)
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if not isinstance(x, list):
        raise TypeErrorException(value=x, expected_type=list)

    results = []
    for item in x:
        try:
            result = f(item)
            results.append(result)
        except Exception as err:
            logger.error((f"{f.__name__}({shorten(str(x), 40)})", str(err)))
            raise err

    return results


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    if not isinstance(x, dict):
        raise TypeErrorException(value=x, expected_type=dict)

    data = {}
    try:
        for key, value in x.items():
            result = f(value)
            data[key] = result
    except Exception as err:
        logger.error((f"{f.__name__}({shorten(str(x), 40)})", str(err)))
        raise err

    return data


def from_union(fs: List[Callable[[Any], T]], x: Any):
    exceptions = []
    for f in fs:
        try:
            return f(x)
        except Exception as err:
            exceptions.append((f"{f.__name__}({shorten(str(x), 40)})", str(err), err))

    logger.error(exceptions[0])
    raise exceptions[0][-1]
