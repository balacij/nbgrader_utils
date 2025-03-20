from .testcase import *


def grade_2d(tests: list[T], failAllOnError: bool = False) -> float:
    return f"{grade(tests, failAllOnError):.2f}"


def grade(tests: list[T], failAllOnError: bool = False) -> float:
    total = 0.0

    has_custom_eval_errors = False

    for t in tests:
        match t.run():
            case S.SUCCESS:
                total += t.value
            case S.FAILED_UNEXPECTED_ERROR:
                if failAllOnError:
                    total = 0.0
                    break
            case S.FAILED_CUSTOM_FUNC_ERROR:
                has_custom_eval_errors = True

        print(t.status_message)

    if has_custom_eval_errors:
        print("⚠️ WARNING: CUSTOM EVALUATOR ERRORED OUT. CHECK LOGS. ⚠️")

    return total
