from typing import Callable
from .testcase import *


def grade(
    tests: list[T],
    statusMessageFormat: Callable = simple_testcase_status_format,
    stopOnFirstFail: bool = False,
    zeroIfAnyError: bool = False,
    warnOnCustomEvaluatorErrors: bool = False,
) -> float:
    total = 0.0

    has_custom_eval_errors = False
    has_errors = False

    for t in tests:
        status = t.run()

        try:
            message = statusMessageFormat(status)
            if message != "":
                print(message)
        except:
            pass

        if status == S.SUCCESS:
            total += t.value
            continue

        if status == S.FAILED_CUSTOM_FUNC_ERROR:
            has_custom_eval_errors = True
            has_errors = True
        elif status == S.FAILED_UNEXPECTED_ERROR:
            has_errors = True

        if stopOnFirstFail:
            break

    if zeroIfAnyError and has_errors:
        total = 0.0
        print("❌ GRADING SUITE FAILED.")

    if warnOnCustomEvaluatorErrors and has_custom_eval_errors:
        print("⚠️ WARNING: CUSTOM EVALUATOR ERRORED OUT. ⚠️")

    return total
