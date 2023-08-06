from typing import Callable


def return_on_failure(f: Callable, v):
    """
    Run f() and return v if f yields any exception in other case it will return f result
    Args:
        f: Callable to be called
        v: Default value to be returned if f raise any exception

    Returns: f result or v.
    """

    try:
        return f()
    except:
        return v
