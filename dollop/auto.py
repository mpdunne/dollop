import io
import pathlib

from typing import Any, Generator
from collections.abc import Sequence as SequenceType

from .sequence import serve as serve_sequence
from .file import serve as serve_file
from .pandas import serve as serve_pandas
from .numpy import serve as serve_numpy
from .torch import serve as serve_torch


def serve(obj: Any, serving_size: int, **kwargs) -> Generator[Any, None, None]:
    """
    Split an iterable of items into a number of smaller iterables, with max serving_size items
    in each. Detect the type automatically and decide how to proceed.

    :param obj: The object that we wish to serve.
    :param serving_size: The max number of items in each outputted subiterable.
    :param kwargs: Any additional arguments to pass to the type-specific function.
    :return:
    """

    if isinstance(obj, SequenceType):
        yield from serve_sequence(obj, serving_size=serving_size)

    elif isinstance(obj, (io.IOBase, pathlib.Path)):
        yield from serve_file(obj, serving_size=serving_size, **kwargs)

    elif obj.__class__.__module__.startswith("pandas"):
        yield from serve_pandas(obj, serving_size=serving_size)

    elif obj.__class__.__module__.startswith("numpy"):
        yield from serve_numpy(obj, serving_size=serving_size, **kwargs)

    elif obj.__class__.__module__.startswith("torch"):
        yield from serve_torch(obj, serving_size=serving_size, **kwargs)

    else:
        raise NotImplementedError(f'Object of type {type(obj)} is not dollopable.')
