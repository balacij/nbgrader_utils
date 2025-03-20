from ..nbgrader_utils import *


def test_eq_tol_good():
    # Values within tolerance
    assert eq_tol(1.00005, 1.0) == True
    assert eq_tol(2.0, 2.001, 0.002) == True

    # Values exactly equivalent
    assert eq_tol(5.0, 5.0) == True

    # Zero tolerance
    assert eq_tol(2.0, 2.0, 0.0) == True


def test_eq_tol_bad():
    # Values outside tolerance
    assert eq_tol(1.1, 1.0) == False
    assert eq_tol(3.0, 3.005, 0.004) == False

    # Zero tolerance
    assert eq_tol(1.0001, 1.0000, 0.0) == False


def test_T_float():
    total = grade(
        [T_float(1.0, "good", "2.0", 2.0), T_float(1.0, "good", "2.00001", 2.0)]
    )
    assert total == 2.0

    total = grade(
        [
            T_float(1.0, "bad", "2.1", 2.0),
            T_float(1.0, "bad", "2.0001", 2.0),
        ]
    )
    assert total == 0.0
