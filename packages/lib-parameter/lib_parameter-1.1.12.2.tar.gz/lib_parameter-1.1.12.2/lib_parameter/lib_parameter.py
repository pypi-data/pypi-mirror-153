from typing import TypeVar, Optional

T = TypeVar("T")


def get_default_if_none(parameter: Optional[T], default: T) -> T:
    """
    Returns default if parameter is None - otherwise return the parameter

    The Parameter has usually the Type Optional[T], the returned type will be type T

    >>> get_default_if_none(parameter=None, default=True)
    True
    >>> get_default_if_none(parameter=False, default=4)
    False
    """
    if parameter is None:
        return default
    else:
        return parameter


if __name__ == "__main__":
    print("this is a library only, the executable is named lib_parameter_cli.py")
