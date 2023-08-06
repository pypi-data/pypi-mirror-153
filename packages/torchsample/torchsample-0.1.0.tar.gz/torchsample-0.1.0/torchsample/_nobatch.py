from functools import wraps

import torch


def _slice_first(obj):
    if isinstance(obj, torch.Tensor):
        return obj[0]
    elif isinstance(obj, list):
        return [_slice_first(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple([_slice_first(x) for x in obj])
    elif isinstance(obj, dict):
        return {k: _slice_first(v) for k, v in obj.items()}
    else:
        return obj


def _expand_first(obj):
    if isinstance(obj, torch.Tensor):
        return obj[None]
    elif isinstance(obj, list):
        return [_expand_first(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple([_expand_first(x) for x in obj])
    elif isinstance(obj, dict):
        return {k: _expand_first(v) for k, v in obj.items()}
    else:
        return obj


def nobatch(f):
    """Return a decorator adapter for batchless tensors.

    Primarily for use in ``Dataset``.

    Adds a ``nobatch`` attribute to the decorated function that:
        1. When invoked, will add a singleton first dimension
           to all tensors passed in.
        2. Will remove the returned singleton dimension in
           returned Tensors.
    """

    def _nobatch(*args, **kwargs):
        args = _expand_first(args)
        kwargs = _expand_first(kwargs)
        out = f(*args, **kwargs)
        return _slice_first(out)

    f.nobatch = _nobatch
    return f
