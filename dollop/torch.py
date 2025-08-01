from typing import Generator, TYPE_CHECKING

from ._utils import calculate_slices

if TYPE_CHECKING:
    import torch # Keep this here for string-based type-checking


def serve(tensor: "torch.Tensor", serving_size: int = None, n_servings: int = None, dim: int = 0) -> \
        Generator["torch.Tensor", None, None]:
    """
    Read a PyTorch tensor small dollops at a time.

    :param tensor: The tensor object.
    :param serving_size: The size of each dollop. Mutually exclusive with n_servings.
    :param n_servings: The number of dollops, of roughly equal size. Mutually exclusive with serving_size.
    :param dim: The dimension along which to slice. Default is 0.
    :return: Generator yielding tensor slices.
    """

    if not (tensor.__class__.__module__.startswith("torch") and tensor.__class__.__name__ == "Tensor"):
        raise TypeError('Dollop torch.serve only supports PyTorch Tensor types.')

    if tensor.ndim == 0:
        raise ValueError("Cannot slice a zero-dimensional (scalar) tensor.")

    if dim < 0 or dim >= tensor.ndim:
        raise ValueError(f"Invalid dim={dim}; tensor has {tensor.ndim} dimensions.")

    slices = calculate_slices(total=tensor.shape[dim], serving_size=serving_size, n_servings=n_servings)

    # Make a view of the array with the chosen dim at the front.
    axes = list(range(tensor.ndim))
    axes[0], axes[dim] = axes[dim], axes[0]
    tensor_permuted = tensor.permute(*axes)

    # Get inverse permutation
    axes_inv = [axes.index(i) for i in range(tensor.ndim)]

    for slc in slices:
        dollop = tensor_permuted[slc]
        yield dollop.permute(*axes_inv)
