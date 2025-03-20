import sys


def steal_scope(
    max_python_frame_depth: int, exact: bool = False, debug: bool = False
) -> tuple[dict, dict]:
    if max_python_frame_depth <= 0:
        raise ValueError("max_python_frame_depth must be a positive integer.")

    try:
        frame = sys._getframe(max_python_frame_depth)

        if debug:
            print(f"Found frame at depth {max_python_frame_depth}")

        return frame.f_globals, frame.f_locals
    except ValueError:
        if debug:
            print(f"Depth {max_python_frame_depth} failed, trying shallower depth.")

        if not exact and max_python_frame_depth > 1:
            return steal_scope(max_python_frame_depth - 1, exact, debug)

        raise IndexError(
            f"Could not find a valid scope within depth {max_python_frame_depth}."
        )
