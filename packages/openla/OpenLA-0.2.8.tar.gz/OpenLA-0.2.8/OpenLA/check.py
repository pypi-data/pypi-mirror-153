import numpy as np


def _is_str(x):
    """
    Check whether the argument is str type or not.

    :param x: The argument to be checked whether str type or not.
    :type x: any type

    :return: Whether argument "x" is string type or not
    :rtype: bool
    """
    return isinstance(x, str)


def _is_str_list(x):
    """
    Check whether the argument is list of str or not.

    :param x: The argument to be checked whether list of str or not.
    :type x: any type

    :return: Whether argument "x" is iterable and all elements have string type, or not
    :rtype: bool
    """
    is_iter = hasattr(x, "__iter__")
    if _is_str(x) or not is_iter:
        return False
    else:
        is_str_elements = all([_is_str(element) for element in x])
        return is_str_elements


def _is_int(x):
    """
    Check whether the argument is int type or not.

    :param x: The argument to be checked whether int type or not.
    :type x: any type

    :return: Whether argument "x" is integer type or not
    :rtype: bool
    """
    return isinstance(x, int) or isinstance(x, np.int64) or isinstance(x, np.int32)


def _is_int_list(x):
    """
    Check whether the argument is list of int or not.

    :param x: The argument to be checked whether list of int or not.
    :type x: any type

    :return: Whether argument "x" is iterable and all elements have integer type, or not
    :rtype: bool
    """
    is_iter = hasattr(x, "__iter__")
    if not is_iter:
        return False
    else:
        is_int_elements = all([_is_int(element) for element in x])
        return is_int_elements
