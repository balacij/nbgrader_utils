from .testcase import *


def eq_tol(v: float, e: float, tol: float = 1e-4):
    return abs(v - e) <= tol


def T_float(
    value: float,
    description: str,
    code: str,
    expect_approx: float,
    expect_error: bool = False,
    ignore_errors: bool = False,
) -> T:
    def within_tol(v):
        return eq_tol(v, expect_approx)

    return T(
        value,
        description,
        code,
        within_tol,
        expect_value_type=float,
        expect_error=expect_error,
        ignore_errors=ignore_errors,
    )
