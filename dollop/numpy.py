from typing import Generator, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy # Keep this here for string-based type-checking


def serve(array: "numpy.ndarray", serving_size: int, dim: int = 0) -> Generator["numpy.ndarray", None, None]:
    """
    Read a NumPy array small chunks at a time.

    :param array: The NumPy array to slice.
    :param serving_size: The number of items per slice.
    :param dim: The dimension along which to slice. Default is 0.
    :return: Generator yielding array slices.
    """
    if not (array.__class__.__module__.startswith("numpy") and array.__class__.__name__ == "ndarray"):
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
