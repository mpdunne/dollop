try:
    import torch
except ImportError:
    raise ImportError('PyTorch installation required to import from dollop.torch')

from typing import Generator


def serve(tensor: torch.Tensor, serving_size: int, dim: int = 0) -> Generator[torch.Tensor, None, None]:
    """
    Read a PyTorch tensor small chunks at a time.

    :param tensor: The tensor object.
    :param serving_size: The max number of items in each serving.
    :param dim: The dimension along which to slice. Default is 0.
    :return: Generator yielding tensor slices.
    """
    if not isinstance(tensor, torch.Tensor):
        raise NotImplementedError('Dollop torch.serve only supports PyTorch tensor types.')

    if tensor.ndim == 0:
        raise ValueError("Cannot slice a zero-dimensional (scalar) tensor.")

    if dim < 0 or dim >= tensor.ndim:
        raise ValueError(f"Invalid dim={dim}; tensor has {tensor.ndim} dimensions.")

    dim_size = tensor.shape[dim]
    for i in range(0, dim_size, serving_size):
        slc = [slice(None)] * tensor.ndim
        slc[dim] = slice(i, i + serving_size)
        yield tensor[tuple(slc)]
