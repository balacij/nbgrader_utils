from ..nbgrader_utils import *


def test_empty():
    total = grade([])
    assert total == 0.0


def test_one_good():
    total = grade([T(1.0, "True is True", "True", True, expectedValType=bool)])
    assert total == 1.0


def test_one_bad():
    total = grade([T(1.0, "False is True", "False", True, expectedValType=bool)])
    assert total == 0.0


def test_simple():
    total = grade(
        [
            T(1.0, "good", "False", True, expectedValType=bool),
            T(1.0, "bad", "False", False, expectedValType=bool),
        ]
    )
    assert total == 1.0


def test_typing():
    total = grade(
        [
            T(1.0, "is empty list", "True", [], expectedValType=list),
            T(1.0, "is empty list", "[]", [], expectedValType=list),
        ]
    )
    assert total == 1.0


def test_error_out():
    total = grade(
        [T(1.0, "1/0 errors", "1/0", expectFail=True), T(1.0, "1/0 errors", "1/0", 0.0)]
    )
    assert total == 1.0
