from datetime import datetime, timezone
from typing import Any, Type, Dict, Tuple, Callable, Union, Optional
import re

from dateutil.parser import parse as parse_datetime


def _match_type(x: Type, y: Type) -> Tuple[bool, bool]:
    if Optional[x] == y:
        return True, True
    if x == y:
        return True, False
    return False, False


def from_sqlite(value: Any, to_type: Type) -> Any:
    from_type = type(value)
    is_none = value is None
    # FIXME
    t, o = _match_type(datetime, to_type)
    if t:
        if from_type == str:
            return parse_datetime(value)
        elif from_type == int or from_type == float:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        elif is_none and o:
            return None
    t, o = _match_type(bool, to_type)
    if t:
        if from_type == int:
            return value == 1
        elif is_none and o:
            return None
    return value


# def from_python(value: Any) -> Any:
#     from_type = type(value)
#     if from_type == datetime:
#         return str(value)
#     return value
