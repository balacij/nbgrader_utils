from ..nbgrader_utils import *


def test_empty():
    total = grade([])
    assert total == 0.0


def test_one_good():
    total = grade([T(1.0, "True is True", "True", True, expect_value_type=bool)])
    assert total == 1.0


def test_one_bad():
    total = grade([T(1.0, "False is True", "False", True, expect_value_type=bool)])
    assert total == 0.0


def test_bools():
    total = grade(
        [
            T(1.0, "== False", "False", False, expect_value_type=bool),
            T(1.0, "== True", "False", True, expect_value_type=bool),
        ]
    )
    assert total == 1.0


def test_typing():
    total = grade(
        [
            T(1.0, "is empty list", "True", [], expect_value_type=list),
            T(1.0, "is empty list", "[]", [], expect_value_type=list),
        ]
    )
    assert total == 1.0


def test_error_out():
    total = grade(
        [
            T(1.0, "1/0 is a ZeroDivisionError", "1/0", expect_error=True),
            T(1.0, "1/0 is 0.0", "1/0", 0.0),
        ]
    )
    assert total == 1.0


def test_any_of():
    def one_of_first_three(v):
        return v in {1, 2, 3}

    total = grade(
        [
            T(
                1.0,
                "1 is one of the first three positive integers (set-based)",
                "1",
                {1, 2, 3},
                int,
            ),
            T(
                1.0,
                "1 is one of the first three positive integers (list-based)",
                "1",
                [1, 2, 3],
                int,
            ),
            T(
                1.0,
                "1 is one of the first three positive integers (list-based)",
                "1",
                one_of_first_three,
                int,
            ),
        ]
    )
    assert total == 3.0
