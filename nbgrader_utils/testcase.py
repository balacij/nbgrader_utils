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
        expectedVal: Any = None,
        expectedValType: Optional[type] = None,
        expectFail: bool = False,
        ignoreErrors: bool = False,
    ):
        assert value > 0.01, "All test cases should be worth at least 0.01"
        self.value = value

        assert len(description) > 0, "All test cases need a description."
        self.description = description

        assert len(code) > 0, "Missing code."
        self.code = code

        assert expectFail or expectedVal is not None, "Need grading criterion."
        if callable(expectedVal):
            assert hasattr(
                expectedVal, "__name__"
            ), "Custom evaluation functions must have a name."
            # TODO: Note assumption: callable expectedVal should never result in an error
        self.expectedVal = expectedVal
        self.expectFail = expectFail

        assert (
            expectedValType is None or type(expectedValType) == type
        ), "Expected value types must be valid types."
        self.expectedValType = expectedValType

        self.ignoreErrors = ignoreErrors
        self.status = None
        self.calculated_val = None

    def run(self) -> Status:
        self.status = self.run0()
        self.status_message = self.status_message0()
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

            if self.expectFail or self.ignoreErrors:
                return S.SUCCESS

            return S.FAILED_UNEXPECTED_ERROR

        if self.expectFail:
            return S.FAILED_EXPECTED_FAILURE

        if not (self.expectedValType is None or isinstance(val, self.expectedValType)):
            return S.FAILED_TYPE_CHECKING

        if callable(self.expectedVal):
            try:
                if self.expectedVal(val):
                    return S.SUCCESS
                else:
                    return S.FAILED_CUSTOM_FUNC_UNSATISFIED
            except Exception as e:
                self.calculated_val = str(e)

            return S.FAILED_CUSTOM_FUNC_ERROR

        if (hasattr(self.expectedVal, "__contains__") and val in self.expectedVal) or (
            val == self.expectedVal
        ):
            return S.SUCCESS

        return S.FAILED_EXPECTED_VALUE

    def status_message0(self) -> Optional[str]:
        if self.status is None:
            return None

        match self.status:
            case S.SUCCESS:
                return f"✅ {self.description}."
            case S.FAILED_TYPE_CHECKING:
                return f"❌ {self.description}. Expected {self.expectedValType.__name__}-typed value, got: {type(self.calculated_val).__name__}"
            case S.FAILED_UNEXPECTED_ERROR:
                return f"❌ {self.description}. Found error on input '{self.code}': {self.calculated_val}"
            case S.FAILED_EXPECTED_VALUE:
                if hasattr(self.expectedVal, "__contains__"):
                    return f"❌ {self.description}. Expected any of {self.expectedVal}, got: {self.calculated_val}"
                else:
                    return f"❌ {self.description}. Expected '{self.expectedVal}', got: {self.calculated_val}"
            case S.FAILED_EXPECTED_FAILURE:
                return (
                    f"❌ {self.description}. Expected error, got: {self.calculated_val}"
                )
            case S.FAILED_CUSTOM_FUNC_UNSATISFIED:
                return f"❌ {self.description}. Test failed custom evaluation: {self.expectedVal.__name__}({self.code})"
            case S.FAILED_CUSTOM_FUNC_ERROR:
                return f"‼️ {self.description}. Custom evaluation function failed with error: {self.calculated_val}"

        return None


T = TestCase
