from typing import Any, Optional
from enum import Enum

from .testcase import *


def grade_2d(tests: list[T], failAllOnErr: bool = False) -> float:
    return f"{grade(tests, failAllOnErr):.2f}"


def grade(tests: list[T], failAllOnErr: bool = False) -> float:
    total = 0.0

    any_errors = False

    has_custom_eval_errors = False

    for t in tests:
        match t.run():
            case S.SUCCESS:
                total += t.value
            case S.FAILED_UNEXPECTED_ERROR:
                if failAllOnErr:
                    total = 0.0
                    break
            case S.FAILED_CUSTOM_FUNC_ERROR:
                has_custom_eval_errors = True

        print(t.status_message)

    if has_custom_eval_errors:
        print("⚠️ WARNING: CUSTOM EVALUATOR ERRORED OUT. CHECK LOGS. ⚠️")

    return total
