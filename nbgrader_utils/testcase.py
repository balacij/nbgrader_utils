from typing import Any, Optional
from enum import Enum


class Status(Enum):
    SUCCESS = 1

    FAILED_TYPE_CHECKING = 10
    FAILED_EXPECTED_VALUE = 11
    FAILED_UNEXPECTED_ERROR = 12

    FAILED_CUSTOM_FUNC = 20
    FAILED_CUSTOM_FUNC_ERROR = 21


S = Status


class TestCase:
    __test__ = False  # stop pytest from discovering this

    def __init__(
        self,
        value: float,
        msg: str,
        code: str,
        expectedVal: Optional[Any] = None,
        expectedValType: Optional[type] = None,
        expectFail: bool = False,
        ignoreErrs: bool = False,
    ):
        self.value = value
        self.msg = msg
        self.code = code
        self.expectedVal = expectedVal
        self.expectedValType = expectedValType
        self.expectFail = expectFail
        self.ignoreErrs = ignoreErrs

        # TODO: warn on value == 0

        # TODO: assert expectedVal is not None or expectFail

        # TODO: if callable expectedVal, then assert there is a __name__

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
            val = eval(self.code)

            self.calculated_val = val
        except Exception as e:
            self.calculated_val = str(e)

            if self.expectFail or self.ignoreErrs:
                return S.SUCCESS

            return S.FAILED_UNEXPECTED_ERROR

        if not (self.expectedValType is None or isinstance(val, self.expectedValType)):
            return S.FAILED_TYPE_CHECKING

        if callable(self.expectedVal):
            try:
                if self.expectedVal(val):
                    return S.SUCCESS
                else:
                    return S.FAILED_CUSTOM_FUNC
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
                return f"✅ {self.msg}."
            case S.FAILED_TYPE_CHECKING:
                return f"❌ {self.msg}. Expected '{self.expectedValType.__name__}'-typed return value, got: {type(self.calculated_val).__name__}"
            case S.FAILED_UNEXPECTED_ERROR:
                return f"❌ {self.msg}. Unexpected error: {self.calculated_val}"
            case S.FAILED_EXPECTED_VALUE:
                if hasattr(self.expectedVal, "__contains__"):
                    return f"❌ {self.msg}. Expected any of {self.expectedVal}, got: {self.calculated_val}"
                else:
                    return f"❌ {self.msg}. Expected '{self.expectedVal}', got: {self.calculated_val}"
            case S.FAILED_CUSTOM_FUNC:
                return f"❌ {self.msg}. Test failed custom evaluation: {self.expectedVal.__name__}({self.code})"
            case S.FAILED_CUSTOM_FUNC_ERROR:
                return f"‼️ {self.msg}. Custom evaluation function failed with error: {self.calculated_val}"

        return None


T = TestCase
