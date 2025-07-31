try:
    import numpy as np
except ImportError:
    raise ImportError('PyTorch installation required to import from dollop.torch')

from typing import Generator


def serve(array: np.ndarray, serving_size: int, dim: int = 0) -> Generator[np.ndarray, None, None]:
    """
    Read a NumPy array small chunks at a time.

    :param array: The NumPy array to slice.
    :param serving_size: The number of items per slice.
    :param dim: The dimension along which to slice. Default is 0.
    :return: Generator yielding array slices.
    """
    if not isinstance(array, np.ndarray):
        raise NotImplementedError('Dollop numpy.serve only supports NumPy ndarray types.')

    if array.ndim == 0:
        raise ValueError("Cannot slice a zero-dimensional (scalar) array.")

    if dim < 0 or dim >= array.ndim:
        raise ValueError(f"Invalid dim={dim}; array has {array.ndim} dimensions.")

    dim_size = array.shape[dim]
    for i in range(0, dim_size, serving_size):
        slc = [slice(None)] * array.ndim
        slc[dim] = slice(i, i + serving_size)
        yield array[tuple(slc)]
