import pandas as pd

from typing import Any, Generator, Iterable
from collections.abc import Sequence as SequenceType

from .sequence import serve as serve_sequence
from .pandas import serve as serve_pandas
# from .file import serve as serve_file


def serve(obj: Any, serving_size: int) -> Generator[Any, None, None]:
    """
    Split an iterable of items into a number of smaller iterables, with max serving_size items
    in each. Detect the type automatically and decide how to proceed.

    :param obj: The object that we wish to serve.
    :param serving_size: The max number of items in each outputted subiterable.
    :return:
    """

    if isinstance(obj, SequenceType):
        yield from serve_sequence(obj, serving_size=serving_size)

    elif isinstance(obj, (pd.DataFrame, pd.Series)):
        yield from serve_pandas(obj, serving_size=serving_size)

    else:
        raise NotImplementedError(f'Object of type {type(obj)} is not dollopable.')
