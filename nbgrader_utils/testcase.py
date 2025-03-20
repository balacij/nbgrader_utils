from typing import Any, Optional
from enum import Enum

import sys


class Status(Enum):
    SUCCESS = 1

    FAILED_TYPE_CHECKING = 10
    FAILED_EXPECTED_VALUE = 11
    FAILED_EXPECTED_FAILURE = 12
    FAILED_UNEXPECTED_ERROR = 13

    FAILED_CUSTOM_FUNC_UNSATISFIED = 20
    FAILED_CUSTOM_FUNC_ERROR = 21


S = Status


class TestCase:
    __test__ = False  # stop pytest from discovering this

    def __init__(
        self,
        value: float,
        description: str,
        code: str,
        expect_value: Any = None,
        expect_value_type: Optional[type] = None,
        expect_error: bool = False,
        ignore_errors: bool = False,
    ):
        assert value > 0.01, "All test cases should be worth at least 0.01"
        self.value = value

        assert len(description) > 0, "All test cases need a description."
        self.description = description

        assert len(code) > 0, "Missing code."
        self.code = code

        assert expect_error or expect_value is not None, "Need grading criterion."
        if callable(expect_value):
            assert hasattr(
                expect_value, "__name__"
            ), "Custom evaluation functions must have a name."
            # TODO: Note assumption: callable expected_value should never result in an error
        self.expected_value = expect_value
        self.expect_error = expect_error

        assert (
            expect_value_type is None or type(expect_value_type) == type
        ), "Expected value types must be valid types."
        self.expect_value_type = expect_value_type

        self.ignore_errors = ignore_errors
        self.status = None
        self.calculated_val = None

    def run(self) -> Status:
        self.status = self.run0()
        return self.status

    def run0(self) -> Status:
        if self.status is not None:
            return self.status

        val = None
        try:
            # Get the caller *before* `grading.py`
            frame = sys._getframe(3)
            caller_globals = frame.f_globals
            caller_locals = frame.f_locals

            # print(f"DEBUG: caller_globals keys: {list(caller_globals.keys())}")
            # print(f"DEBUG: caller_locals keys: {list(caller_locals.keys())}")

            val = eval(self.code, caller_globals, caller_locals)
            self.calculated_val = val
        except Exception as e:
            self.calculated_val = f"{e} ({type(e).__name__})"

            if self.expect_error or self.ignore_errors:
                return S.SUCCESS

            return S.FAILED_UNEXPECTED_ERROR

        if self.expect_error:
            return S.FAILED_EXPECTED_FAILURE

        if not (
            self.expect_value_type is None or isinstance(val, self.expect_value_type)
        ):
            return S.FAILED_TYPE_CHECKING

        if callable(self.expected_value):
            try:
                if self.expected_value(val):
                    return S.SUCCESS
                else:
                    return S.FAILED_CUSTOM_FUNC_UNSATISFIED
            except Exception as e:
                self.calculated_val = str(e)

            return S.FAILED_CUSTOM_FUNC_ERROR

        if (
            hasattr(self.expected_value, "__contains__") and val in self.expected_value
        ) or (val == self.expected_value):
            return S.SUCCESS

        return S.FAILED_EXPECTED_VALUE


T = TestCase
TC = TestCase


def simple_testcase_status_format(tc: T) -> str:
    match tc.status:
        case S.SUCCESS:
            return f"✅ {tc.description}."
        case S.FAILED_TYPE_CHECKING:
            return f"❌ {tc.description}. Expected {tc.expect_value_type.__name__}-typed value, got: {type(tc.calculated_val).__name__}"
        case S.FAILED_UNEXPECTED_ERROR:
            return f"❌ {tc.description}. Found error on input '{tc.code}': {tc.calculated_val}"
        case S.FAILED_EXPECTED_VALUE:
            if hasattr(tc.expected_value, "__contains__"):
                return f"❌ {tc.description}. Expected any of {tc.expected_value}, got: {tc.calculated_val}"
            else:
                return f"❌ {tc.description}. Expected '{tc.expected_value}', got: {tc.calculated_val}"
        case S.FAILED_EXPECTED_FAILURE:
            return f"❌ {tc.description}. Expected error, got: {tc.calculated_val}"
        case S.FAILED_CUSTOM_FUNC_UNSATISFIED:
            return f"❌ {tc.description}. Test failed custom evaluation: {tc.expected_value.__name__}({tc.code})"
        case S.FAILED_CUSTOM_FUNC_ERROR:
            return f"‼️ {tc.description}. Custom evaluation function failed with error: {tc.calculated_val}"

    assert (
        False
    ), "Incomplete status pattern match simple_testcase_status_format implementation."
