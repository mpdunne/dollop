import numpy as np
import pytest

import torch
from dollop.torch import serve

sizes = (
    (1,),
    (10,),
    (100,),
    (100, 100, 10),
    (101, 99, 67),
    (101, 1, 67),
    (101, 1, 67, 902),
    (20, 20, 20, 20),
    (1, 1, 1, 1, 1, 1),
)

arrays = [torch.rand(size) for size in sizes]


@pytest.mark.parametrize("tensor", arrays)
@pytest.mark.parametrize("dim", list(range(5)))
@pytest.mark.parametrize("serving_size", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_torch(tensor, dim, serving_size):
    if tensor.ndim <= dim:
        with pytest.raises(ValueError):
            _ = [*serve(tensor, serving_size=serving_size, dim=dim)]
        return

    size = tensor.shape[dim]
    other_dims = [i for i in range(tensor.ndim) if i != dim]
    other_shapes = [tensor.shape[i] for i in other_dims]

    dollops = [*serve(tensor, serving_size=serving_size, dim=dim)]

    expected_full = size // serving_size
    remainder = size % serving_size

    if remainder == 0:
        assert len(dollops) == expected_full
        assert all(d.shape[dim] == serving_size for d in dollops)
    else:
        assert len(dollops) == expected_full + 1
        assert all(d.shape[dim] == serving_size for d in dollops[:-1])
        assert dollops[-1].shape[dim] == remainder

    for d in dollops:
        for i, shape in zip(other_dims, other_shapes):
            assert d.shape[i] == shape, f"Mismatch on dim {i}: expected {shape}, got {d.shape[i]}"

    recon = torch.cat(dollops, dim=dim)
    np.testing.assert_array_equal(recon.numpy(), tensor.numpy())
    assert all(isinstance(d, torch.Tensor) for d in dollops)


def test_serve_torch_0d_tensor_raises():
    scalar = torch.tensor(42)
    with pytest.raises(ValueError):
        _ = [*serve(scalar, serving_size=1)]


@pytest.mark.parametrize("bad_input", [
    [1, 2, 3],
    (1, 2, 3),
    10,
    10.5,
    None,
])
def test_serve_torch_non_tensor_obj_raises_error(bad_input):
    with pytest.raises(TypeError):
        _ = [*serve(bad_input, serving_size=5)]
