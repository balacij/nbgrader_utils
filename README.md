# `nbgrader_utils`

Supplementing `nbgrader` with unit test-based partial grading.

## Installation

Make sure you have `nbgrader` installed (it is not installed automatically with
this package), then install this package:

> pip install git+https://github.com/balacij/nbgrader_utils.git#egg=nbgrader_utils

## Quick Start

Create a fresh assignment with nbgrader, and end an auto-graded test cell with
the following code:
```python
from nbgrader_utils import T, grade

# Use `T(...)` to define individual tests, and `grade([T1, T2, ...])` to run
# them. For example:

grade([
    T(0.5, "1/0 is a ZeroDivisionError", "1/0", expect_error=True),
    T(0.5, "1/0 is 0", "1/0", 0),
    T(1, "1/1 is 1", "1/1", 1),
])
# End of cell
```

Generate and release the assignment, and then submit, collect, and auto-grade a
copy. You should find that your submission results in 1.5/2 marks assigned.

## Documentation

Full documentation is not yet available, but if this library gains users, it
will be written. In the meantime, you can explore the code directly:
* [`grading.py`](./nbgrader_utils/grading.py) (specifically, `def grade(...)`).
* [`testcase.py`](./nbgrader_utils/testcase.py) (specifically, `TestCase.__init__(...)`).

If you'd like, you can also have a peek at the [few unit tests](./tests/) too.

## License

This software is licensed under the [`GPL`](./LICENSE) license.
