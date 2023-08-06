#!/usr/bin/env python
import arrow
import pytest
from pytest_lazyfixture import lazy_fixture

from oomnitza_rule_checker.checker import (DatePeriod, Op,
                                           _convert_string_to_timestamp,
                                           _get_prop_from_field, _is_iterable,
                                           _is_json, _is_numeric, _missed,
                                           check_rule_by_op, check_rules)


@pytest.mark.parametrize(
    "given_field,given_object_type,expected_result",
    [
        ("ASSETS.serial_number", "ASSETS", "serial_number"),
        ("ASSETS.serial_number", "assets", "ASSETS.serial_number"),
        ("ASSETS.serial_number", "WHATEVER", "ASSETS.serial_number"),
        ("ASSETS.serial_number", "", "ASSETS.serial_number"),
        ("serial_number", "", "serial_number"),
        ("assigned_to.first_name", "", "assigned_to.first_name"),
     ],
)
def test_get_prop_from_field(given_field, given_object_type, expected_result):
    given_prop = _get_prop_from_field(given_field, given_object_type)
    assert given_prop == expected_result


class TestIsNumeric:
    def test_is_numeric_w_int(self):
        assert _is_numeric(42)

    def test_is_numeric_w_float(self):
        assert _is_numeric(42.0)

    def test_is_numeric_w_none(self):
        assert not _is_numeric(None)

    def test_is_numeric_w_text(self):
        assert not _is_numeric("hello")

    def test_is_numeric_w_int_string(self):
        assert _is_numeric("42")


class TestIsIterable:
    @pytest.mark.parametrize("data_type_value", [(), (1,), [], [1], "", "abc", {}, {"a": "a"}, set(), set('abc')])
    def test_is_iterable_true(self, data_type_value):
        assert _is_iterable(data_type_value)

    @pytest.mark.parametrize("data_type_value", [None, 1, -1.0, True, False])
    def test_is_iterable_false(self, data_type_value):
        assert not _is_iterable(data_type_value)


class TestIsJson:
    @pytest.mark.parametrize("data_value", ['{}', '{"name": "Rabih"}', '{"bool": true}', '{"int": 1}'])
    def test_is_json_true(self, data_value):
        assert _is_json(data_value)

    @pytest.mark.parametrize("data_value", [None, 0, 1, True, False, {}, {"age": 20}, "abc", "", (), (1,)])
    def test_is_json_false(self, data_value):
        assert not _is_json(data_value)


class TestConvertStringToTimestamp:
    def test_ok(self):
        assert _convert_string_to_timestamp("2018/01/01") == 1514764800

    def test_invalid_date_string_not_ok(self):
        with pytest.raises(ValueError):
            _convert_string_to_timestamp("unknown")


class TestCheckRule:
    def test_rule_equal(self):
        assert check_rule_by_op(Op.EQUAL, "a", "a")
        assert not check_rule_by_op(Op.EQUAL, "a", "b")

    def test_rule_not_equal(self):
        assert check_rule_by_op(Op.NOT_EQUAL, "a", "b")
        assert not check_rule_by_op(Op.NOT_EQUAL, "a", "a")

    @pytest.mark.parametrize("left_side, right_side", [(["a"], ["a"]), (["a"], ["a", "b"]), (["a", "b"], ["a", "b"]), (["a", "b"], ["b", "a"]), (["a", "b", "c"], ["a", "b"]), (["a", "b"], ["b", "c"])])
    def test_rule_include_true(self, left_side, right_side):
        assert check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('["a"]', '["a"]'), ('["a"]', '["a", "b"]'), ('["a", "b"]', '["a", "b"]'), ('["a", "b"]', '["b", "a"]'), ('["a", "b", "c"]', '["a", "b"]'), ('["a", "b"]', '["b", "c"]')])
    def test_rule_include_with_json_string_true(self, left_side, right_side):
        assert check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [({"a": "a"}, {"a": "a", "b": "b"}), ("a", "ab"), (("a",), ("a", "b",))])
    def test_rule_include_with_other_iterable_data_types_true(self, left_side, right_side):
        assert check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [(1, 1), (None, None), (True, True)])
    def test_rule_include_with_none_iterable_data_types_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [(["a"], []), (["a"], ["b"])])
    def test_rule_not_include_true(self, left_side, right_side):
        assert check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('["a"]', '[]'), ('["a"]', '["b"]')])
    def test_rule_not_include_with_json_string_true(self, left_side, right_side):
        assert check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [({"a": "a"}, {}), ("a", "b"), (("c",), ("a", "b",))])
    def test_rule_not_include_with_other_iterable_data_types_true(self, left_side, right_side):
        assert check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [(1, 12), (1, None), (True, False)])
    def test_rule_not_include_with_none_iterable_data_types_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [([], []), ([], ["a"]), (["a"], ["b"]), (["a"], [])])
    def test_rule_include_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('[]', '[]'), ('[]', '["a"]'), ('["a"]', '["b"]'), ('["a"]', '[]')])
    def test_rule_include_with_json_string_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [([], []), ([], ["a"]), (["a"], ["a"]), (["a"], ["a", "b"]), (["a", "b"], ["a", "b"]), (["a", "b"], ["b", "a"]), (["a", "b", "c"], ["a", "b"]), (["a", "b"], ["b", "c"])])
    def test_rule_not_include_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('[]', '[]'), ('[]', '["a"]'), ('["a"]', '["a"]'), ('["a"]', '["a", "b"]'), ('["a", "b"]', '["a", "b"]'), ('["a", "b"]', '["b", "a"]'), ('["a", "b", "c"]', '["a", "b"]'), ('["a", "b"]', '["b", "c"]')])
    def test_rule_not_include_with_json_string_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [(["a"], ["a"]), (["a"], ["a", "b"]), (["a", "b"], ["a", "b"]), (["a", "b"], ["b", "a"])])
    def test_rule_strict_include_true(self, left_side, right_side):
        assert check_rule_by_op(Op.STRICT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('["a"]', '["a"]'), ('["a"]', '["a", "b"]'), ('["a", "b"]', '["a", "b"]'), ('["a", "b"]', '["b", "a"]')])
    def test_rule_strict_include_with_json_string_true(self, left_side, right_side):
        assert check_rule_by_op(Op.STRICT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [(["a"], []), (["a"], ["b"]), (["a", "b", "c"], ["a", "b"]), (["a", "b"], ["b", "c"])])
    def test_rule_strict_not_include_true(self, left_side, right_side):
        assert check_rule_by_op(Op.STRICT_NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('["a"]', '[]'), ('["a"]', '["b"]'), ('["a", "b", "c"]', '["a", "b"]'), ('["a", "b"]', '["b", "c"]')])
    def test_rule_strict_not_include_with_json_string_true(self, left_side, right_side):
        assert check_rule_by_op(Op.STRICT_NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [([], []), ([], ["a"]), (["a"], ["b"]), (["a", "b", "c"], ["a", "b"]), (["a", "b"], ["b", "c"]), (["a"], [])])
    def test_rule_strict_include_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.STRICT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('[]', '[]'), ('[]', '["a"]'), ('["a"]', '["b"]'), ('["a", "b", "c"]', '["a", "b"]'), ('["a", "b"]', '["b", "c"]'), ('["a"]', '[]')])
    def test_rule_strict_include_with_json_string_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.STRICT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [([], []), ([], ["a"]), (["a"], ["a"]), (["a"], ["a", "b"]), (["a", "b"], ["a", "b"]), (["a", "b"], ["b", "a"])])
    def test_rule_strict_not_include_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.STRICT_NOT_INCLUDE, left_side, right_side)

    @pytest.mark.parametrize("left_side, right_side", [('[]', '[]'), ('[]', '["a"]'), ('["a"]', '["a"]'), ('["a"]', '["a", "b"]'), ('["a", "b"]', '["a", "b"]'), ('["a", "b"]', '["b", "a"]')])
    def test_rule_strict_not_include_with_json_string_false(self, left_side, right_side):
        assert not check_rule_by_op(Op.STRICT_NOT_INCLUDE, left_side, right_side)

    def test_rule_begins_with(self):
        assert check_rule_by_op(Op.BEGINS_WITH, "aaa", "a")
        assert not check_rule_by_op(Op.BEGINS_WITH, "aaa", "b")

    def test_rule_does_not_begin_with(self):
        assert not check_rule_by_op(Op.DOES_NOT_BEGIN_WITH, "aaa", "a")
        assert check_rule_by_op(Op.DOES_NOT_BEGIN_WITH, "aaa", "b")

    def test_rule_ends_with(self):
        assert check_rule_by_op(Op.ENDS_WITH, "aaa", "a")
        assert not check_rule_by_op(Op.ENDS_WITH, "aaa", "b")

    def test_rule_does_not_end_with(self):
        assert not check_rule_by_op(Op.DOES_NOT_END_WITH, "aaa", "a")
        assert check_rule_by_op(Op.DOES_NOT_END_WITH, "aaa", "b")

    def test_rule_contains(self):
        assert check_rule_by_op(Op.CONTAINS, "aaa", "a")
        assert not check_rule_by_op(Op.CONTAINS, "aaa", "b")

    def test_rule_does_not_contain(self):
        assert not check_rule_by_op(Op.DOES_NOT_CONTAIN, "aaa", "a")
        assert check_rule_by_op(Op.DOES_NOT_CONTAIN, "aaa", "b")

    def test_rule_lt(self):
        assert check_rule_by_op(Op.LESS_THEN, "1", "2")
        assert not check_rule_by_op(Op.LESS_THEN, "2", "1")

    def test_rule_le(self):
        assert check_rule_by_op(Op.LESS_OR_EQUAL, "1", "2")
        assert check_rule_by_op(Op.LESS_OR_EQUAL, "2", "2")

    def test_rule_gt(self):
        assert check_rule_by_op(Op.GREATER_THEN, "2", "1")
        assert not check_rule_by_op(Op.GREATER_THEN, "1", "2")

    def test_rule_ge(self):
        assert check_rule_by_op(Op.GREATER_OR_EQUAL, "2", "2")
        assert check_rule_by_op(Op.GREATER_OR_EQUAL, "3", "2")

    def test_rule_lt_0_value(self):
        assert check_rule_by_op(Op.LESS_THEN, "0", "2")
        assert not check_rule_by_op(Op.LESS_THEN, "2", "0")

    def test_rule_le_0_value(self):
        assert check_rule_by_op(Op.LESS_OR_EQUAL, "0.1", "2")
        assert check_rule_by_op(Op.LESS_OR_EQUAL, "0", "0")
        assert not check_rule_by_op(Op.LESS_OR_EQUAL, "0.2", "0.1")

    def test_rule_gt_0_value(self):
        assert check_rule_by_op(Op.GREATER_THEN, "2", "0")
        assert not check_rule_by_op(Op.GREATER_THEN, "0", "0.001")

    def test_rule_ge_0_value(self):
        assert check_rule_by_op(Op.GREATER_OR_EQUAL, "0.0000001", "0")
        assert check_rule_by_op(Op.GREATER_OR_EQUAL, "0", "0")
        assert not check_rule_by_op(Op.GREATER_OR_EQUAL, "0", "0.2")

    @pytest.mark.parametrize(
        "operator,left_value,right_value",
        [
            (Op.LESS_THEN, "invalid", "2"),
            (Op.LESS_THEN, "2", "0.1.0"),
            (Op.LESS_OR_EQUAL, "invalid", "2"),
            (Op.LESS_OR_EQUAL, "0", "0000.1.0000"),
            (Op.LESS_OR_EQUAL, "0.1.0", "@!#$"),
            (Op.GREATER_THEN, "2", "invalid"),
            (Op.GREATER_THEN, "0", "0.001*)"),
            (Op.GREATER_OR_EQUAL, "invalid", "invalid"),
            (Op.GREATER_OR_EQUAL, "0.0001", "0.0001*"),
        ],
    )
    def test_invalid_numeric_value(self, operator, left_value, right_value):
        assert not check_rule_by_op(operator, left_value, right_value)

    @pytest.mark.parametrize("left_value", [None, "", []])
    def test_rule_is_null(self, left_value):
        assert check_rule_by_op(Op.IS_NULL, left_value, None)

    @pytest.mark.parametrize("left_value", ["1", [1]])
    def test_rule_not_null(self, left_value):
        assert check_rule_by_op(Op.NOT_NULL, left_value, None)

    @pytest.fixture
    def now(self):
        return arrow.utcnow()

    @pytest.fixture
    def now_unix(self, now):
        return now.timestamp

    @pytest.fixture
    def day_before_unix(self, now):
        return now.shift(days=-1).timestamp

    @pytest.fixture
    def day_before_at_13_30_unix(self, now):
        return now.shift(days=-1).replace(hour=13, minute=30).timestamp

    @pytest.fixture
    def day_before_at_8_20_unix(self, now):
        return now.shift(days=-1).replace(hour=8, minute=20).timestamp

    @pytest.fixture
    def day_before_at_23_59_unix(self, now):
        return now.shift(days=-1).replace(hour=23, minute=59).timestamp

    @pytest.fixture
    def day_after_unix(self, now):
        return now.shift(days=1).timestamp

    @pytest.fixture
    def day_after_at_13_30_unix(self, now):
        return now.shift(days=1).replace(hour=13, minute=30).timestamp

    @pytest.fixture
    def day_after_at_8_20_unix(self, now):
        return now.shift(days=1).replace(hour=8, minute=20).timestamp

    @pytest.fixture
    def day_after_at_23_59_unix(self, now):
        return now.shift(days=1).replace(hour=23, minute=59).timestamp

    @pytest.mark.parametrize(
        "current_value,target_value,expected_result",
        [
            (lazy_fixture("day_before_unix"), "1", True),
            (lazy_fixture("day_before_at_8_20_unix"), "1", True),
            (lazy_fixture("day_before_at_13_30_unix"), "1", True),
            (lazy_fixture("day_before_at_23_59_unix"), "1", True),
            (lazy_fixture("day_before_unix"), "2", False),
            (None, "2", False),
        ],
    )
    def test_rule_days_after_ok(self, current_value, target_value, expected_result):
        given_result = check_rule_by_op(Op.DAYS_AFTER, current_value, target_value)
        assert bool(given_result) is expected_result

    @pytest.mark.parametrize(
        "current_value,target_value,expected_result",
        [
            (lazy_fixture("day_after_unix"), "1", True),
            (lazy_fixture("day_after_at_8_20_unix"), "1", True),
            (lazy_fixture("day_after_at_13_30_unix"), "1", True),
            (lazy_fixture("day_after_at_23_59_unix"), "1", True),
            (lazy_fixture("day_after_unix"), "2", False),
            (None, "1", False),
            (None, "2", False),
        ],
    )
    def test_rule_days_before_ok(self, current_value, target_value, expected_result):
        given_result = check_rule_by_op(Op.DAYS_BEFORE, current_value, target_value)
        assert bool(given_result) is expected_result

    def test_rule_days_equal_ok(self, now_unix):
        assert check_rule_by_op(Op.DAYS_EQUAL, f"{now_unix}", None)
        assert not check_rule_by_op(Op.DAYS_EQUAL, None, None)

    def test_rule_has_been_changed_ok(self):
        assert check_rule_by_op(Op.HAS_BEEN_CHANGED, "before", "after")
        assert not check_rule_by_op(Op.HAS_BEEN_CHANGED, "dontcare", "dontcare")
        assert check_rule_by_op(Op.HAS_BEEN_CHANGED, _missed, "after")
        assert not check_rule_by_op(Op.HAS_BEEN_CHANGED, "before", _missed)
        assert not check_rule_by_op(Op.HAS_BEEN_CHANGED, _missed, _missed)

    def test_rule_between_ok(self, now_unix, day_before_unix, day_after_unix):
        assert not check_rule_by_op(
            Op.BETWEEN, f"{now_unix}", {"from": day_after_unix, "to": None},
        )
        assert not check_rule_by_op(
            Op.BETWEEN, f"{now_unix}", {"from": None, "to": day_before_unix},
        )
        assert check_rule_by_op(
            Op.BETWEEN, f"{now_unix}", {"from": day_before_unix, "to": day_after_unix},
        )
        assert check_rule_by_op(
            Op.BETWEEN, f"{now_unix}", {"from": day_before_unix, "to": None},
        )
        assert check_rule_by_op(
            Op.BETWEEN, f"{now_unix}", {"from": None, "to": day_after_unix},
        )

    def test_rule_unknown_action_not_ok(self):
        assert not check_rule_by_op("unknown_action", None, None)

    @pytest.fixture
    def two_day_before_unix(self, now):
        return now.shift(days=-2).timestamp

    @pytest.fixture
    def two_day_after_unix(self, now):
        return now.shift(days=2).timestamp

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("day_before_unix"), "", True),
            (lazy_fixture("day_before_at_8_20_unix"), "", True),
            (lazy_fixture("day_before_at_13_30_unix"), "", True),
            (lazy_fixture("day_before_at_23_59_unix"), "", True),
            (lazy_fixture("two_day_before_unix"), "", False),

            (lazy_fixture("day_before_unix"), "trash", True),
            (None, "", False),
            ('asdsa', "", False),
        ],
    )
    def test_day_before_current_date(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.DAY_BEFORE_CURRENT_DATE, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("day_after_unix"), "", True),
            (lazy_fixture("day_after_at_8_20_unix"), "", True),
            (lazy_fixture("day_after_at_13_30_unix"), "", True),
            (lazy_fixture("day_after_at_23_59_unix"), "", True),
            (lazy_fixture("two_day_after_unix"), "", False),

            (lazy_fixture("day_after_unix"), "trash", True),
            (None, "", False),
            ('asdsa', "", False),
        ],
    )
    def test_day_after_current_date(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.DAY_AFTER_CURRENT_DATE, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.fixture
    def week_before_unix(self, now):
        return now.shift(weeks=-1).timestamp

    @pytest.fixture
    def two_week_before_unix(self, now):
        return now.shift(weeks=-2).timestamp

    @pytest.fixture
    def week_after_unix(self, now):
        return now.shift(weeks=1).timestamp

    @pytest.fixture
    def two_week_after_unix(self, now):
        return now.shift(weeks=2).timestamp

    @pytest.fixture
    def month_before_unix(self, now):
        return now.shift(months=-1).timestamp

    @pytest.fixture
    def two_month_before_unix(self, now):
        return now.shift(months=-2).timestamp

    @pytest.fixture
    def month_after_unix(self, now):
        return now.shift(months=1).timestamp

    @pytest.fixture
    def two_month_after_unix(self, now):
        return now.shift(months=2).timestamp

    @pytest.fixture
    def quarter_before_unix(self, now):
        return now.shift(quarters=-1).timestamp

    @pytest.fixture
    def two_quarter_before_unix(self, now):
        return now.shift(quarters=-2).timestamp

    @pytest.fixture
    def quarter_after_unix(self, now):
        return now.shift(quarters=1).timestamp

    @pytest.fixture
    def two_quarter_after_unix(self, now):
        return now.shift(quarters=2).timestamp

    @pytest.fixture
    def year_before_unix(self, now):
        return now.shift(years=-1).timestamp

    @pytest.fixture
    def two_year_before_unix(self, now):
        return now.shift(years=-2).timestamp

    @pytest.fixture
    def year_after_unix(self, now):
        return now.shift(years=1).timestamp

    @pytest.fixture
    def two_year_after_unix(self, now):
        return now.shift(years=2).timestamp

    @pytest.fixture
    def week_start_factory(self, now):
        return lambda offset: now.replace(days=1).floor('week').replace(weeks=offset).replace(days=-1).timestamp

    @pytest.fixture
    def month_start_factory(self, now):
        return lambda offset: now.floor('month').replace(months=offset).timestamp

    @pytest.fixture
    def quarter_start_factory(self, now):
        return lambda offset: now.floor('quarter').replace(quarters=offset).timestamp

    @pytest.fixture
    def year_start_factory(self, now):
        return lambda offset: now.floor('year').replace(years=offset).timestamp

    @pytest.fixture
    def week_last_positive_corner_case(self, week_start_factory):
        return week_start_factory(-1)

    @pytest.fixture
    def week_last_negative_corner_case(self, week_last_positive_corner_case):
        return week_last_positive_corner_case - 1

    @pytest.fixture
    def month_last_positive_corner_case(self, month_start_factory):
        return month_start_factory(-1)

    @pytest.fixture
    def month_last_negative_corner_case(self, month_last_positive_corner_case):
        return month_last_positive_corner_case - 1

    @pytest.fixture
    def quarter_last_positive_corner_case(self, quarter_start_factory):
        return quarter_start_factory(-1)

    @pytest.fixture
    def quarter_last_negative_corner_case(self, quarter_last_positive_corner_case):
        return quarter_last_positive_corner_case - 1

    @pytest.fixture
    def year_last_positive_corner_case(self, year_start_factory):
        return year_start_factory(-1)

    @pytest.fixture
    def year_last_negative_corner_case(self, year_last_positive_corner_case):
        return year_last_positive_corner_case - 1

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("week_before_unix"), DatePeriod.WEEK, True),
            (lazy_fixture("two_week_before_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_after_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_last_positive_corner_case"), DatePeriod.WEEK, True),
            (lazy_fixture("week_last_negative_corner_case"), DatePeriod.WEEK, False),

            (lazy_fixture("month_before_unix"), DatePeriod.MONTH, True),
            (lazy_fixture("two_month_before_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_after_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_last_positive_corner_case"), DatePeriod.MONTH, True),
            (lazy_fixture("month_last_negative_corner_case"), DatePeriod.MONTH, False),

            (lazy_fixture("quarter_before_unix"), DatePeriod.QUARTER, True),
            (lazy_fixture("two_quarter_before_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_after_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_last_positive_corner_case"), DatePeriod.QUARTER, True),
            (lazy_fixture("quarter_last_negative_corner_case"), DatePeriod.QUARTER, False),

            (lazy_fixture("year_before_unix"), DatePeriod.YEAR, True),
            (lazy_fixture("two_year_before_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_after_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_last_positive_corner_case"), DatePeriod.YEAR, True),
            (lazy_fixture("year_last_negative_corner_case"), DatePeriod.YEAR, False),

            (lazy_fixture("week_before_unix"), "trash", False),
            (None, "", False),
            ('asdsa', "", False),
        ],
    )
    def test_last(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.LAST, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.fixture
    def week_next_positive_corner_case(self, week_start_factory):
        return week_start_factory(1)

    @pytest.fixture
    def week_next_negative_corner_case(self, week_next_positive_corner_case):
        return week_next_positive_corner_case - 1

    @pytest.fixture
    def month_next_positive_corner_case(self, month_start_factory):
        return month_start_factory(1)

    @pytest.fixture
    def month_next_negative_corner_case(self, month_next_positive_corner_case):
        return month_next_positive_corner_case - 1

    @pytest.fixture
    def quarter_next_positive_corner_case(self, quarter_start_factory):
        return quarter_start_factory(1)

    @pytest.fixture
    def quarter_next_negative_corner_case(self, quarter_next_positive_corner_case):
        return quarter_next_positive_corner_case - 1

    @pytest.fixture
    def year_next_positive_corner_case(self, year_start_factory):
        return year_start_factory(1)

    @pytest.fixture
    def year_next_negative_corner_case(self, year_next_positive_corner_case):
        return year_next_positive_corner_case - 1

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("week_after_unix"), DatePeriod.WEEK, True),
            (lazy_fixture("two_week_after_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_before_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_next_positive_corner_case"), DatePeriod.WEEK, True),
            (lazy_fixture("week_next_negative_corner_case"), DatePeriod.WEEK, False),

            (lazy_fixture("month_after_unix"), DatePeriod.MONTH, True),
            (lazy_fixture("two_month_after_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_before_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_next_positive_corner_case"), DatePeriod.MONTH, True),
            (lazy_fixture("month_next_negative_corner_case"), DatePeriod.MONTH, False),

            (lazy_fixture("quarter_after_unix"), DatePeriod.QUARTER, True),
            (lazy_fixture("two_quarter_after_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_before_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_next_positive_corner_case"), DatePeriod.QUARTER, True),
            (lazy_fixture("quarter_next_negative_corner_case"), DatePeriod.QUARTER, False),

            (lazy_fixture("year_after_unix"), DatePeriod.YEAR, True),
            (lazy_fixture("two_year_after_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_before_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_next_positive_corner_case"), DatePeriod.YEAR, True),
            (lazy_fixture("year_next_negative_corner_case"), DatePeriod.YEAR, False),

            (lazy_fixture("week_after_unix"), "trash", False),
            (None, "", False),
            ('asdsa', "", False),
        ],
    )
    def test_next(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.NEXT, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.fixture
    def week_this_positive_corner_case(self, week_start_factory):
        return week_start_factory(0)

    @pytest.fixture
    def week_this_negative_corner_case(self, week_this_positive_corner_case):
        return week_this_positive_corner_case - 1

    @pytest.fixture
    def month_this_positive_corner_case(self, month_start_factory):
        return month_start_factory(0)

    @pytest.fixture
    def month_this_negative_corner_case(self, month_this_positive_corner_case):
        return month_this_positive_corner_case - 1

    @pytest.fixture
    def quarter_this_positive_corner_case(self, quarter_start_factory):
        return quarter_start_factory(0)

    @pytest.fixture
    def quarter_this_negative_corner_case(self, quarter_this_positive_corner_case):
        return quarter_this_positive_corner_case - 1

    @pytest.fixture
    def year_this_positive_corner_case(self, year_start_factory):
        return year_start_factory(0)

    @pytest.fixture
    def year_this_negative_corner_case(self, year_this_positive_corner_case):
        return year_this_positive_corner_case - 1

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("now_unix"), DatePeriod.WEEK, True),
            (lazy_fixture("week_after_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_before_unix"), DatePeriod.WEEK, False),
            (lazy_fixture("week_this_positive_corner_case"), DatePeriod.WEEK, True),
            (lazy_fixture("week_this_negative_corner_case"), DatePeriod.WEEK, False),

            (lazy_fixture("now_unix"), DatePeriod.MONTH, True),
            (lazy_fixture("month_after_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_before_unix"), DatePeriod.MONTH, False),
            (lazy_fixture("month_this_positive_corner_case"), DatePeriod.MONTH, True),
            (lazy_fixture("month_this_negative_corner_case"), DatePeriod.MONTH, False),

            (lazy_fixture("now_unix"), DatePeriod.QUARTER, True),
            (lazy_fixture("quarter_after_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_before_unix"), DatePeriod.QUARTER, False),
            (lazy_fixture("quarter_this_positive_corner_case"), DatePeriod.QUARTER, True),
            (lazy_fixture("quarter_this_negative_corner_case"), DatePeriod.QUARTER, False),

            (lazy_fixture("now_unix"), DatePeriod.YEAR, True),
            (lazy_fixture("year_after_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_before_unix"), DatePeriod.YEAR, False),
            (lazy_fixture("year_this_positive_corner_case"), DatePeriod.YEAR, True),
            (lazy_fixture("year_this_negative_corner_case"), DatePeriod.YEAR, False),

            (lazy_fixture("now_unix"), "trash", False),
            (None, "", False),
            ('asdsa', "", False),
        ],
    )
    def test_this(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.THIS, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.fixture
    def two_day_before_at_23_59_unix(self, now):
        return now.shift(days=-2).replace(hour=23, minute=59).timestamp

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("day_after_unix"), '{"days": 1, "condition": "after"}', True),
            (lazy_fixture("day_after_at_8_20_unix"), '{"days": 1, "condition": "after"}', True),
            (lazy_fixture("day_after_at_13_30_unix"), '{"days": 1, "condition": "after"}', True),
            (lazy_fixture("day_after_at_23_59_unix"), '{"days": 1, "condition": "after"}', True),
            (lazy_fixture("two_day_after_unix"), '{"days": 1, "condition": "after"}', True),
            (lazy_fixture("two_day_after_unix"), '{"days": 2, "condition": "after"}', True),
            (lazy_fixture("day_after_at_23_59_unix"), '{"days": 2, "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), '{"days": 2, "condition": "after"}', False),

            (lazy_fixture("day_before_unix"), '{"days": 1, "condition": "before"}', True),
            (lazy_fixture("day_before_at_8_20_unix"), '{"days": 1, "condition": "before"}', True),
            (lazy_fixture("day_before_at_13_30_unix"), '{"days": 1, "condition": "before"}', True),
            (lazy_fixture("day_before_at_23_59_unix"), '{"days": 1, "condition": "before"}', True),
            (lazy_fixture("day_before_at_23_59_unix"), '{"days": 2, "condition": "before"}', True),
            (lazy_fixture("two_day_before_unix"), '{"days": 2, "condition": "before"}', True),
            (lazy_fixture("day_before_unix"), '{"days": 2, "condition": "before"}', True),
            (lazy_fixture("two_day_before_unix"), '{"days": 1, "condition": "before"}', False),
            (lazy_fixture("two_day_before_at_23_59_unix"), '{"days": 1, "condition": "before"}', False),

            (None, '{"days": 1, "condition": "after"}', False),
            ('asdsa', '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), None, False),
            (lazy_fixture("day_after_unix"), '{"days": "asda", "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), '{"days": 1, "condition": "asdas"}', False),
            (lazy_fixture("day_after_unix"), 'ffssaf{', False),
        ],
    )
    def test_after(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.AFTER, current_value, data)
        assert bool(given_result) is expected_result

    @pytest.mark.parametrize(
        "current_value,data,expected_result",
        [
            (lazy_fixture("day_after_unix"), '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("day_after_at_8_20_unix"), '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("day_after_at_13_30_unix"), '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("day_after_at_23_59_unix"), '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("two_day_after_unix"), '{"days": 1, "condition": "after"}', False),
            (lazy_fixture("two_day_after_unix"), '{"days": 2, "condition": "after"}', False),
            (lazy_fixture("day_after_at_23_59_unix"), '{"days": 2, "condition": "after"}', True),
            (lazy_fixture("day_after_unix"), '{"days": 2, "condition": "after"}', True),

            (lazy_fixture("day_before_unix"), '{"days": 1, "condition": "before"}', False),
            (lazy_fixture("day_before_at_8_20_unix"), '{"days": 1, "condition": "before"}', False),
            (lazy_fixture("day_before_at_13_30_unix"), '{"days": 1, "condition": "before"}', False),
            (lazy_fixture("day_before_at_23_59_unix"), '{"days": 1, "condition": "before"}', False),
            (lazy_fixture("day_before_at_23_59_unix"), '{"days": 2, "condition": "before"}', False),
            (lazy_fixture("two_day_before_unix"), '{"days": 2, "condition": "before"}', False),
            (lazy_fixture("day_before_unix"), '{"days": 2, "condition": "before"}', False),
            (lazy_fixture("two_day_before_unix"), '{"days": 1, "condition": "before"}', True),
            (lazy_fixture("two_day_before_at_23_59_unix"), '{"days": 1, "condition": "before"}', True),
            #
            (None, '{"days": 2, "condition": "after"}', False),
            ('asdsa', '{"days": 2, "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), None, False),
            (lazy_fixture("day_after_unix"), '{"days": "asda", "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), '{"days": 1, "condition": "asdas"}', False),
            (lazy_fixture("day_after_unix"), '{"days": "asda", "condition": "after"}', False),
            (lazy_fixture("day_after_unix"), 'asdf', False),
        ],
    )
    def test_before(self, current_value, data, expected_result):
        given_result = check_rule_by_op(Op.BEFORE, current_value, data)
        assert bool(given_result) is expected_result


class TestCheckRules:
    @pytest.fixture
    def rules_w_data(self):
        return [
            {"op": "cn", "data": "CC1UH", "field": "ASSETS.serial_number",},
            {
                "op": "eq",
                "data": "2e84e8e99431411a84f2339bd02cacb0",
                "field": "ASSETS.assigned_to",
            },
            {
                "op": "eq",
                "data": "ad2c2ab54adb481c8436d6238838813a",
                "field": "ASSETS.equipment_id",
            },
        ]

    @pytest.fixture
    def rules_wo_data_field(self):
        return [
            {
                "op": "nu",
                "field": "ASSETS.serial_number"
            },
            {
                "op": "nu",
                "field": "ASSETS.assigned_to",
            },
        ]

    @pytest.fixture
    def group_w_rule_wo_data_field(self, rules_wo_data_field):
        some_rule, *rest = rules_wo_data_field
        return {
            "rules": [],
            "groupOp": "and",
            "groups": [
                {"groupOp": "and", "rules": [some_rule, ], "groups": [], },
                {"groupOp": "and", "rules": [*rest], "groups": [], },
            ],
        }

    @pytest.fixture
    def group_w_andop(self, rules_w_data):
        some_rule, *rest = rules_w_data
        return {
            "rules": [],
            "groupOp": "and",
            "groups": [
                {"groupOp": "and", "rules": [some_rule,], "groups": [],},
                {"groupOp": "and", "rules": [*rest], "groups": [],},
            ],
        }

    @pytest.fixture
    def group_w_orop(self, rules_w_data):
        some_rule, *rest = rules_w_data
        return {
            "rules": [],
            "groupOp": "or",
            "groups": [
                {"groupOp": "and", "rules": [some_rule,], "groups": [],},
                {"groupOp": "and", "rules": [*rest], "groups": [],},
            ],
        }

    @pytest.fixture
    def document(self):
        return {
            "equipment_id": "ad2c2ab54adb481c8436d6238838813a",
            "assigned_to": "2e84e8e99431411a84f2339bd02cacb0",
            "serial_number": "C02CC1UHMD6T1",
            "model": "MacBookPro16,1",
        }

    @pytest.fixture
    def document_w_partial_match(self, document):
        return {
            "equipment_id": "9cd3ed7e80a0467f89bbc715ef4d8609",
            "assigned_to": "5ae18391b46344ca9d88dd857dc2f21f",
            "serial_number": "C02CC1UHMD6T2",
            "model": "MacBookPro16,1",
        }

    @pytest.mark.parametrize(
        "given_rules,given_document,expected_result",
        [
            (
                lazy_fixture("group_w_andop"),
                lazy_fixture("document"),
                True,
            ),
            (
                lazy_fixture("group_w_andop"),
                lazy_fixture("document_w_partial_match"),
                False,
            ),
            (
                lazy_fixture("group_w_andop"),
                {},
                False,
            ),
            (
                lazy_fixture("group_w_orop"),
                lazy_fixture("document"),
                True,
            ),
            (
                lazy_fixture("group_w_orop"),
                lazy_fixture("document_w_partial_match"),
                True,
            ),
            (
                lazy_fixture("group_w_orop"),
                {},
                False,
            ),
            (
                lazy_fixture("group_w_rule_wo_data_field"),
                lazy_fixture("document"),
                False
            )
        ],
    )
    def test_ok(self, given_rules, given_document, expected_result):
        given_result = check_rules(
            given_rules,
            document=given_document,
            changed_values=None,
            object_type="ASSETS",
        )
        assert given_result is expected_result
