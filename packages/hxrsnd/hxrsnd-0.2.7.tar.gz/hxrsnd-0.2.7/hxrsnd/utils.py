"""
Script for small utility functions used in HXRSnD
"""
import inspect
import logging
from collections.abc import Iterable
from functools import wraps
from math import nan
from pathlib import Path

logger = logging.getLogger(__name__)


def absolute_submodule_path(submodule, cur_dir=inspect.stack()[0][1]):
    """
    Returns the absolute path of the inputted SnD submodule based on an inputted
    absolute path, or the absolute path of this file.

    Parameters
    ----------
    submodule : str or Path
        Desired submodule path.

    cur_dir : str or Path, optional
        Absolute path to use as a template for the full submodule path.

    Returns
    -------
    full_path : str
        Full string path to the inputted submodule.
    """
    dir_parts = Path(cur_dir).parts
    sub_parts = Path(submodule).parts
    base_path = Path(*dir_parts[:dir_parts.index(sub_parts[0])])
    if str(base_path) == ".":
        logger.warning("Could not match base path with desired submodule.")
    full_path = base_path / Path(submodule)
    return str(full_path)


def as_list(obj, length=None, tp=None, iter_to_list=True):
    """
    Force an argument to be a list, optionally of a given length, optionally
    with all elements cast to a given type if not None.

    Parameters
    ---------
    obj : Object
        The obj we want to convert to a list.

    length : int or None, optional
        Length of new list. Applies if the inputted obj is not an iterable and
        iter_to_list is false.

    tp : type, optional
        Type to cast the values inside the list as.

    iter_to_list : bool, optional
        Determines if we should cast an iterable (not str) obj as a list or to
        enclose it in one.

    Returns
    -------
    obj : list
        The object enclosed or cast as a list.
    """
    # If the obj is None, return empty list or fixed-length list of Nones
    if obj is None:
        if length is None:
            return []
        return [None] * length

    # If it is already a list do nothing
    elif isinstance(obj, list):
        pass

    # If it is an iterable (and not str), convert it to a list
    elif isiterable(obj) and iter_to_list:
        obj = list(obj)

    # Otherwise, just enclose in a list making it the inputted length
    else:
        try:
            obj = [obj] * length
        except TypeError:
            obj = [obj]

    # Cast to type; Let exceptions here bubble up to the top.
    if tp is not None:
        obj = [tp(o) for o in obj]
    return obj


def isiterable(obj):
    """
    Function that determines if an object is an iterable, not including
    str.

    Parameters
    ----------
    obj : object
        Object to test if it is an iterable.

    Returns
    -------
    bool : bool
        True if the obj is an iterable, False if not.
    """
    if isinstance(obj, str):
        return False
    else:
        return isinstance(obj, Iterable)


def _flatten(inp_iter):
    """
    Recursively iterate through values in nested iterables.

    Parameters
    ----------
    inp_iter : iterable
        The iterable to flatten.

    Returns
    -------
    value : object
        The contents of the iterable
    """
    for val in inp_iter:
        if isiterable(val):
            for ival in _flatten(val):
                yield ival
        else:
            yield val


def flatten(inp_iter):
    """
    Returns a flattened list of the inputted iterable.

    Parameters
    ----------
    inp_iter : iterable
        The iterable to flatten.

    Returns
    -------
    flattened_iter : list
        The contents of the iterable as a flat list
    """
    return list(_flatten(inp_iter))


def stop_on_keyboardinterrupt(func):
    """
    Decorator that runs the object's `stop` method if a keyboard interrupt is
    raised. This is meant to be used on ophyd device methods and expects the
    first argument to be `self`.
    """
    @wraps(func)
    def stop_dev_on_keyboardinterrupt(obj, *args, **kwargs):
        if hasattr(obj, "stop") and callable(obj.stop):
            try:
                return func(obj, *args, **kwargs)
            except KeyboardInterrupt:
                obj.stop()
                logger.info("Motor '{0}' stopped by keyboard interrupt".format(
                    obj.name))
        else:
            raise AttributeError("Object '{0}' needs a stop method to use the "
                                 "stop_on_keyboardinterrupt decorator.".format(
                                     obj))
    return stop_dev_on_keyboardinterrupt


def nan_if_no_parent(method):
    """
    Decorator that will return None if the object passed via self does not have
    a parent.
    """
    @wraps(method)
    def inner(obj, *args, **kwargs):
        if obj.parent:
            return method(obj, *args, **kwargs)
        else:
            return nan
    return inner
