import numpy as np
import pytest

from dollop.numpy import serve

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

arrays = [np.random.random(size=size) for size in sizes]


@pytest.mark.parametrize("array", arrays)
@pytest.mark.parametrize("dim", [*range(5)])
@pytest.mark.parametrize("serving_size", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_numpy_by_serving_size(array, dim, serving_size):

    if array.ndim <= dim:
        with pytest.raises(ValueError):
            _ = [*serve(array, serving_size=serving_size, dim=dim)]
        return

    size = array.shape[dim]
    other_dims = [i for i in range(array.ndim) if i != dim]
    other_shapes = [array.shape[i] for i in other_dims]

    dollops = [*serve(array, serving_size=serving_size, dim=dim)]

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

    recon = np.concatenate(dollops, axis=dim)
    np.testing.assert_array_equal(recon, array)
    assert all(isinstance(d, np.ndarray) for d in dollops)


@pytest.mark.parametrize("array", arrays)
@pytest.mark.parametrize("dim", [*range(5)])
@pytest.mark.parametrize("n_servings", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_numpy_by_n_servings(array, dim, n_servings):

    if array.ndim <= dim:
        with pytest.raises(ValueError):
            _ = [*serve(array, n_servings=n_servings, dim=dim)]
        return

    size = array.shape[dim]
    other_dims = [i for i in range(array.ndim) if i != dim]
    other_shapes = [array.shape[i] for i in other_dims]

    dollops = [*serve(array, n_servings=n_servings, dim=dim)]
    assert len(dollops) == n_servings

    max_size = size // n_servings + 1
    assert all(d.shape[dim] in (max_size - 1, max_size) for d in dollops)
    assert all(isinstance(d, np.ndarray) for d in dollops)

    for d in dollops:
        for i, shape in zip(other_dims, other_shapes):
            assert d.shape[i] == shape, f"Mismatch on dim {i}: expected {shape}, got {d.shape[i]}"

    recon = np.concatenate(dollops, axis=dim)
    np.testing.assert_array_equal(recon, array)


def test_serve_numpy_0d_array_raises():
    scalar = np.array(42)

    with pytest.raises(ValueError):
        _ = [*serve(scalar, serving_size=1)]

    with pytest.raises(ValueError):
        _ = [*serve(scalar, n_servings=1)]


@pytest.mark.parametrize("bad_input", [
    [1, 2, 3],
    (1, 2, 3),
    10,
    10.5,
    None,
])
def test_serve_numpy_non_numpy_obj_raises_error(bad_input):
    with pytest.raises(TypeError):
        _ = [*serve(bad_input, serving_size=5)]

    with pytest.raises(TypeError):
        _ = [*serve(bad_input, n_servings=5)]
