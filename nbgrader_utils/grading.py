from typing import Callable
from .testcase import *


def grade(
    tests: list[T],
    status_message_formatter: Callable[[S], str] = simple_testcase_status_format,
    stop_on_first_fail: bool = False,
    zero_if_any_error: bool = False,
    warn_on_custom_evaluator_errors: bool = False,
) -> float:
    total = 0.0

    has_custom_eval_errors = False
    has_errors = False

    for t in tests:
        status = t.run()

        try:
            message = status_message_formatter(status)
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

        if stop_on_first_fail:
            break

    if zero_if_any_error and has_errors:
        total = 0.0
        print("❌ GRADING SUITE FAILED.")

    if warn_on_custom_evaluator_errors and has_custom_eval_errors:
        print("⚠️ WARNING: CUSTOM EVALUATOR ERRORED OUT. ⚠️")

    return total
