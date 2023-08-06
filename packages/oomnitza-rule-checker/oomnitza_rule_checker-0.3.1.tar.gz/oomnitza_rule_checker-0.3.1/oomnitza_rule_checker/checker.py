import json
import logging
from collections.abc import Iterable
from itertools import chain
from typing import Any, Dict, Optional, Union

import arrow

from oomnitza_rule_checker.helpers import DateHelper

__all__ = (
    "Op",
    "GroupOperation",
    "FieldDataType",
    "check_rules",
    "check_rule_by_op",
)


RuleType = Dict[str, Any]
DocumentType = Dict[str, Any]
LeftValueType = Optional[Union[str, int, float]]
RightValueType = Optional[Union[str, int, float, Dict[str, Any]]]


class GroupOperation:
    OR = "or"
    AND = "and"


class FieldDataType:
    DATE = "DATE"
    DATETIME = "DATETIME"


class Op:
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    LESS_THEN = "lt"
    LESS_OR_EQUAL = "le"
    GREATER_THEN = "gt"
    GREATER_OR_EQUAL = "ge"
    BEGINS_WITH = "bw"
    DOES_NOT_BEGIN_WITH = "nb"
    ENDS_WITH = "ew"
    DOES_NOT_END_WITH = "nw"
    CONTAINS = "cn"
    DOES_NOT_CONTAIN = "nc"
    IS_NULL = "nu"
    NOT_NULL = "nn"
    DAYS_AFTER = "da"
    DAYS_BEFORE = "db"
    DAYS_EQUAL = "do"
    HAS_BEEN_CHANGED = "hc"
    BETWEEN = "between"
    DAY_BEFORE_CURRENT_DATE = "day_before_current_date"
    DAY_AFTER_CURRENT_DATE = "day_after_current_date"
    LAST = "last"
    THIS = "this"
    NEXT = "next"
    BEFORE = "before"
    AFTER = "after"
    INCLUDE = "in"
    NOT_INCLUDE = "ni"
    STRICT_INCLUDE = "sin"
    STRICT_NOT_INCLUDE = "sni"


class DatePeriod:
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

    @classmethod
    def get_available_periods(cls):
        return [cls.WEEK, cls.MONTH, cls.QUARTER, cls.YEAR]


DATE_ACTIONS = [
    Op.DAYS_AFTER,
    Op.DAYS_BEFORE,
    Op.DAYS_EQUAL,
    Op.IS_NULL,
    Op.NOT_NULL,
    Op.BETWEEN,
]


logger = logging.getLogger(__name__)


_missed = object()

_oomnitza_version_key = "version"
_key_groupop = "groupOp"
_key_field = "field"


def _get_oomnitza_document_version(document: DocumentType) -> int:
    return int(document.get(_oomnitza_version_key, 0))


def _is_initial_document_version(document: DocumentType) -> bool:
    return _get_oomnitza_document_version(document) == 0


def _convert_string_to_timestamp(date_string: str) -> int:
    try:
        return arrow.get(date_string).timestamp
    except:
        raise ValueError


def _is_numeric(value: Any) -> bool:
    """
    Simple method that check whether value can be converted to float.
    """
    try:
        float(value)
    except Exception:
        return False
    return True


def _is_iterable(value: Any) -> bool:
    """
    Simple method that check whether the data type is iterable.
    """
    return isinstance(value, Iterable)


def _is_json(value: Any) -> bool:
    """
    Simple method that check whether the data type is json.
    """
    try:
        json.loads(value)
    except:
        return False
    return True


def check_rule_by_op(
    op: str,
    current_value: LeftValueType,
    target_value: RightValueType,
) -> bool:
    """
    Check current and target values according with the specified
    action type.
    """
    # prepare values
    left_value = (
        current_value.lower() if isinstance(current_value, str) else current_value
    )
    right_value = (
        target_value.lower() if isinstance(target_value, str) else target_value
    )

    if op in (
        Op.EQUAL,
        Op.NOT_EQUAL,
    ):
        if _is_numeric(left_value):
            left_value = float(left_value)
        elif not left_value:
            left_value = None

        if _is_numeric(right_value):
            right_value = float(right_value)
        elif not right_value:
            right_value = None

        if op == Op.EQUAL:
            return left_value == right_value
        elif op == Op.NOT_EQUAL:
            return left_value != right_value

    if op in (
        Op.INCLUDE,
        Op.STRICT_INCLUDE,
        Op.NOT_INCLUDE,
        Op.STRICT_NOT_INCLUDE,
    ):

        if _is_json(left_value):
            left_value = json.loads(left_value)

        if _is_json(right_value):
            right_value = json.loads(right_value)

        if (
            not _is_iterable(left_value) or not _is_iterable(right_value)
        ) or not left_value:
            return False

        if op == Op.INCLUDE:
            return any(item in right_value for item in left_value)
        elif op == Op.STRICT_INCLUDE:
            return all(item in right_value for item in left_value)
        elif op == Op.NOT_INCLUDE:
            return not any(item in right_value for item in left_value)
        elif op == Op.STRICT_NOT_INCLUDE:
            return not all(item in right_value for item in left_value)

    if op in (
        Op.LESS_THEN,
        Op.LESS_OR_EQUAL,
        Op.GREATER_THEN,
        Op.GREATER_OR_EQUAL,
    ):
        if _is_numeric(left_value):
            left_value = float(left_value)
        else:
            return False

        if _is_numeric(right_value):
            right_value = float(right_value)
        else:
            return False

        numeric_operation_mapping = {
            Op.LESS_THEN: lambda a, b: a < b,
            Op.LESS_OR_EQUAL: lambda a, b: a <= b,
            Op.GREATER_THEN: lambda a, b: a > b,
            Op.GREATER_OR_EQUAL: lambda a, b: a >= b,
        }
        return numeric_operation_mapping[op](left_value, right_value)

    elif op in (
        Op.BEGINS_WITH,
        Op.DOES_NOT_BEGIN_WITH,
        Op.ENDS_WITH,
        Op.DOES_NOT_END_WITH,
        Op.CONTAINS,
        Op.DOES_NOT_CONTAIN,
    ):
        # Handling case, when empty / nullable strings
        if not right_value:
            if op in (Op.BEGINS_WITH, Op.ENDS_WITH, Op.CONTAINS):
                # 'apple' begins with / ends with / contains '' -> False)
                return False
            else:
                # 'apple' DOES NOT begin with / end with / contain '' -> True)
                return True

        if not left_value:
            if op in (Op.BEGINS_WITH, Op.ENDS_WITH, Op.CONTAINS):
                # '' begins  with / ends with / contains 'apple' -> False)
                return False
            else:
                # '' DOES NOT begin with / end with / contain 'apple' -> True)
                return True

        left_value = str(left_value).lower()
        right_value = str(right_value).lower()

        substring_operation_mapping = {
            Op.CONTAINS: lambda a, b: b in a,
            Op.DOES_NOT_CONTAIN: lambda a, b: b not in a,
            Op.BEGINS_WITH: lambda a, b: a.startswith(b),
            Op.DOES_NOT_BEGIN_WITH: lambda a, b: not a.startswith(b),
            Op.ENDS_WITH: lambda a, b: a.endswith(b),
            Op.DOES_NOT_END_WITH: lambda a, b: not a.endswith(b),
        }
        return substring_operation_mapping[op](left_value, right_value)

    elif op == Op.IS_NULL:
        return left_value in [None, "", []]

    elif op == Op.NOT_NULL:
        return left_value not in [None, "", []]

    elif op == Op.BETWEEN:
        # it is expected the right value has the form of json dumped string of '{"from": X, "to": Y}'
        # where X and Y are the border values given for the date field
        left_value = int(left_value) if _is_numeric(left_value) else left_value

        if not isinstance(right_value, dict):
            try:
                right_value = json.loads(right_value) if right_value else right_value
            except:
                return False

        if (
            left_value is not None
            and right_value is not None
            and isinstance(left_value, int)
            and isinstance(right_value, dict)
        ):
            from_value: Optional[str] = right_value.get("from")
            to_value: Optional[str] = right_value.get("to")

            if from_value is None:
                return _is_numeric(to_value) and left_value <= int(to_value)

            if to_value is None:
                return _is_numeric(from_value) and int(from_value) <= left_value

            return (
                _is_numeric(from_value)
                and _is_numeric(to_value)
                and int(from_value) <= left_value <= int(to_value)
            )

        return False

    elif op in (
        Op.DAYS_AFTER,
        Op.DAYS_BEFORE,
        Op.DAYS_EQUAL,
    ):
        left_value = int(left_value) if _is_numeric(left_value) else left_value
        right_value = int(right_value) if _is_numeric(right_value) else right_value
        now = arrow.utcnow()

        if op == Op.DAYS_AFTER:
            return (
                left_value
                and (right_value or right_value == 0)
                and DateHelper.get_day_start(now, offset=-right_value)
                <= left_value
                < DateHelper.get_day_start(now, offset=-(right_value - 1))
            )

        if op == Op.DAYS_BEFORE:
            return (
                left_value
                and (right_value or right_value == 0)
                and DateHelper.get_day_start(now, offset=right_value)
                <= left_value
                < DateHelper.get_day_start(now, offset=right_value + 1)
            )

        if op == Op.DAYS_EQUAL:
            return left_value and DateHelper.get_day_start(
                now, offset=-0
            ) <= left_value < DateHelper.get_day_start(now, offset=1)

    elif op == Op.HAS_BEEN_CHANGED:
        # Note: testing the passed in values directly, because left_value and
        # right_value are lowercase strings at this point.
        return target_value is not _missed and current_value != target_value

    elif op in (
        Op.DAY_BEFORE_CURRENT_DATE,
        Op.DAY_AFTER_CURRENT_DATE,
        Op.LAST,
        Op.THIS,
        Op.NEXT,
    ):
        if not _is_numeric(left_value) or (
            op in (Op.LAST, Op.NEXT, Op.THIS)
            and right_value not in DatePeriod.get_available_periods()
        ):
            return False

        interval_offsets = {
            Op.DAY_BEFORE_CURRENT_DATE: (-1, 0),
            Op.DAY_AFTER_CURRENT_DATE: (1, 2),
            Op.THIS: (0, 1),
            Op.NEXT: (1, 2),
            Op.LAST: (-1, 0),
        }

        if op in [
            Op.DAY_BEFORE_CURRENT_DATE,
            Op.DAY_AFTER_CURRENT_DATE,
        ]:
            right_value = DatePeriod.DAY

        now = arrow.utcnow()
        _from, _to = interval_offsets[op]
        return (
            DateHelper.get_start(right_value, now, offset=_from)
            <= int(left_value)
            < DateHelper.get_start(right_value, now, offset=_to)
        )

    elif op in (Op.BEFORE, Op.AFTER):
        if not isinstance(right_value, dict):
            try:
                right_value = json.loads(right_value) if right_value else right_value
            except:
                return False

        if (
            not _is_numeric(left_value)
            or not isinstance(right_value, dict)
            or right_value.get("condition") not in (Op.BEFORE, Op.AFTER)
            or not _is_numeric(right_value.get("days"))
        ):
            return False

        operation_mapping = {
            Op.BEFORE: lambda a, b: a < b,
            Op.AFTER: lambda a, b: a > b,
        }
        days = int(right_value["days"])
        return operation_mapping[op](
            int(left_value),
            DateHelper.get_day_start(
                arrow.utcnow(),
                offset=days if right_value["condition"] == Op.AFTER else -days,
            ),
        )

    return False


def _check_rules_for_group(
    rules: RuleType,
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    if rules[_key_groupop] == GroupOperation.AND:
        for rule in chain(rules["groups"], rules["rules"]):
            has_match = check_rules(rule, document, changed_values, object_type)
            if not has_match:
                return False

        return True

    elif rules[_key_groupop] == GroupOperation.OR:
        for rule in chain(rules["groups"], rules["rules"]):
            has_match = check_rules(rule, document, changed_values, object_type)
            if has_match:
                return True

        return False

    return False


def _get_prop_from_field(field_name: str, object_type: str) -> str:
    delim = f"{object_type}."
    if field_name.startswith(delim):
        unused, prop = field_name.split(delim, 1)
    else:
        prop = field_name
    return prop


def _check_rules_for_rule(
    rules: RuleType,
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    op = rules.get("op")
    value = rules.get("data", "")
    field_name = rules.get("field")
    item_type = rules.get("type")

    if not field_name or not op:
        return False

    prop = _get_prop_from_field(field_name, object_type)

    if isinstance(document, tuple):
        # is this achievable?
        flag = False

        for item in document[object_type]:
            if prop in item and check_rule_by_op(op, item[prop], value):
                flag = True
        return flag

    else:
        if item_type == FieldDataType.DATE and op not in DATE_ACTIONS:
            if value:
                try:
                    value = _convert_string_to_timestamp(value)

                    if op in [
                        Op.LESS_THEN,
                        Op.LESS_OR_EQUAL,
                    ]:
                        day_without_second = 86399  # noqa
                        value += day_without_second

                    value = str(value)
                except ValueError:
                    logger.warning(f"{value!r} is not a valid date!")
                    return False

        if item_type == FieldDataType.DATETIME:
            try:
                if value:
                    value = str(_convert_string_to_timestamp(value))
            except ValueError:
                logger.warning(f"{value!r} is not a valid date!")
                return False

        if op == Op.HAS_BEEN_CHANGED:
            if not _is_initial_document_version(document):
                value = changed_values and changed_values.get(prop, _missed)
            else:
                value = _missed

        if prop not in document:
            logger.warning(
                f"There is no field {object_type}.{prop}. Probably it was deleted."
            )
            return False

        current_value = document.get(prop)

        return check_rule_by_op(op, current_value, value)


def check_rules(
    rules: Optional[RuleType],
    document: DocumentType,
    changed_values: Optional[DocumentType],
    object_type: str,
) -> bool:
    args = [rules, document, changed_values, object_type]
    has_match = True

    if rules is None:
        return has_match
    elif _key_groupop in rules:
        return _check_rules_for_group(*args)
    elif _key_field in rules:
        return _check_rules_for_rule(*args)
    else:
        return has_match
