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
        raise TypeError('Dollop numpy.serve only supports NumPy ndarray types.')

    if array.ndim == 0:
        raise ValueError("Cannot slice a zero-dimensional (scalar) array.")

    if dim < 0 or dim >= array.ndim:
        raise ValueError(f"Specified dim ({dim}) must be smaller than the number of array dimensions ({array.ndim})")

    # Make a view of the array with the chosen dim at the front.
    axes = list(range(array.ndim))
    axes[0], axes[dim] = axes[dim], axes[0]
    array_permutated = array.transpose(axes)

    # Get inverse permutation
    axes_inv = [axes.index(i) for i in range(array.ndim)]

    for i in range(0, len(array_permutated), serving_size):
        dollop = array_permutated[i: i + serving_size]
        yield dollop.transpose(axes_inv)
