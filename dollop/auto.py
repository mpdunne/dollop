import io
import pathlib

from typing import Any, Generator
from collections.abc import Sequence as SequenceType

from .sequence import serve as serve_sequence
from .file import serve as serve_file
from .pandas import serve as serve_pandas
from .numpy import serve as serve_numpy
from .torch import serve as serve_torch


def serve(obj: Any, serving_size: int = None, n_servings: int = None, **kwargs) -> Generator[Any, None, None]:
    """
    Split an object into a series of smaller chunks, either by fixed serving size or by number of servings.

    Exactly one of `serving_size` or `n_servings` must be specified.

    - If `serving_size` is given, each output will contain up to that many items (the last may be smaller).
    - If `n_servings` is given, the input will be split into that many chunks, as evenly as possible.


    :param obj: The object that we wish to serve.
    :param serving_size: The max number of items in each outputted subiterable. Mutually exclusive with n_servings.
    :param n_servings: The number of (almost equal-sized) servings to serve. Mutually exclusive with serving_size.
    :param kwargs: Any additional arguments to pass to the type-specific function.
    :return:
    """

    if isinstance(obj, SequenceType):
        yield from serve_sequence(obj, serving_size=serving_size, n_servings=n_servings, **kwargs)

    elif obj.__class__.__module__.startswith("pandas"):
        yield from serve_pandas(obj, serving_size=serving_size, n_servings=n_servings, **kwargs)

    elif obj.__class__.__module__.startswith("numpy"):
        yield from serve_numpy(obj, serving_size=serving_size, n_servings=n_servings, **kwargs)

    elif obj.__class__.__module__.startswith("torch"):
        yield from serve_torch(obj, serving_size=serving_size, n_servings=n_servings, **kwargs)

    elif isinstance(obj, (io.IOBase, pathlib.Path)):
        if n_servings is not None:
            raise ValueError('Files and IO streams cannot be dolloped using n_servings. Use serving_size instead.')
        else:
            yield from serve_file(obj, serving_size=serving_size, **kwargs)

    else:
        raise NotImplementedError(f'Object of type {type(obj)} is not dollopable.')
