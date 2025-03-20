from .testcase import *


def eq_tol(v: float, e: float, tol: float = 1e-4):
    return abs(v - e) <= tol


def T_float(
    value: float,
    description: str,
    code: str,
    approxExpectedValue: float,
    expectFailure: bool = False,
    ignoreErrors: bool = False,
) -> T:
    def within_tol(v):
        return eq_tol(v, approxExpectedValue)

    return T(
        value,
        description,
        code,
        within_tol,
        expectedValType=float,
        expectFail=expectFailure,
        ignoreErrs=ignoreErrors,
    )
