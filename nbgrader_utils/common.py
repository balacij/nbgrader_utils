from .testcase import *


def eq_tol(v: float, e: float, tol: float = 1e-4):
    return abs(v - e) <= tol
