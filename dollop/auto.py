import io
import pathlib

from typing import Any, Generator
from collections.abc import Sequence as SequenceType

from .sequence import serve as serve_sequence
from .file import serve as serve_file

try:
    import pandas as pd
    from .pandas import serve as serve_pandas
    pandas_installed = True
except ImportError:
    pandas_installed = False

try:
    import numpy as np
    from .numpy import serve as serve_numpy
    numpy_installed = True
except ImportError:
    numpy_installed = False

try:
    import torch
    from .torch import serve as serve_torch
    torch_installed = True
except ImportError:
    torch_installed = False


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

    elif isinstance(obj, (io.IOBase, pathlib.Path)):
        yield from serve_file(obj, serving_size=serving_size)

    elif pandas_installed and isinstance(obj, (pd.DataFrame, pd.Series)):
        yield from serve_pandas(obj, serving_size=serving_size)

    elif numpy_installed and isinstance(obj, (np.ndarray)):
        yield from serve_numpy(obj, serving_size=serving_size)

    elif torch_installed and isinstance(obj, (torch.Tensor)):
        yield from serve_torch(obj, serving_size=serving_size)

    else:
        raise NotImplementedError(f'Object of type {type(obj)} is not dollopable.')
