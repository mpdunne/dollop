from typing import Generator, TYPE_CHECKING

if TYPE_CHECKING:
    import torch # Keep this here for string-based type-checking


def serve(tensor: "torch.Tensor", serving_size: int, dim: int = 0) -> Generator["torch.Tensor", None, None]:
    """
    Read a PyTorch tensor small chunks at a time.

    :param tensor: The tensor object.
    :param serving_size: The max number of items in each serving.
    :param dim: The dimension along which to slice. Default is 0.
    :return: Generator yielding tensor slices.
    """
    if not (tensor.__class__.__module__.startswith("torch") and tensor.__class__.__name__ == "Tensor"):
        raise TypeError('Dollop torch.serve only supports PyTorch Tensor types.')

    if tensor.ndim == 0:
        raise ValueError("Cannot slice a zero-dimensional (scalar) tensor.")

    if dim < 0 or dim >= tensor.ndim:
        raise ValueError(f"Invalid dim={dim}; tensor has {tensor.ndim} dimensions.")

    # Make a view of the array with the chosen dim at the front.
    axes = list(range(tensor.ndim))
    axes[0], axes[dim] = axes[dim], axes[0]
    tensor_permuted = tensor.permute(*axes)

    # Get inverse permutation
    axes_inv = [axes.index(i) for i in range(tensor.ndim)]

    for i in range(0, tensor_permuted.shape[0], serving_size):
        dollop = tensor_permuted[i: i + serving_size]
        yield dollop.permute(*axes_inv)
