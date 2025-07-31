import pytest

from dollop.sequence import serve


@pytest.fixture
def sequence_creators():

    def create_list(n):
        return list(range(n))

    def create_tuple(n):
        return tuple(range(n))

    def create_string(n):
        return 'a' * n

    def create_range(n):
        return range(n)

    def create_bytes(n):
        return bytes(n)

    def create_bytearray(n):
        return bytearray(n)

    return {
        'list': create_list,
        'tuple': create_tuple,
        'str': create_string,
        'range': create_range,
        'bytes': create_bytes,
        'bytearray': create_bytearray,
    }


@pytest.fixture
def non_sequences():
    return {
        'int': 10,
        'float': 10.1,
        'none': None,
    }


@pytest.mark.parametrize('sequence_type', ('list', 'tuple', 'str', 'range', 'bytes', 'bytearray'))
@pytest.mark.parametrize("n_items", (0, 5, 10, 13, 17, 25, 50, 100))
@pytest.mark.parametrize("serving_size", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_sequence_by_serving_size(n_items, serving_size, sequence_type, sequence_creators):

    create_sequence = sequence_creators[sequence_type]

    items = create_sequence(n=n_items)
    dollops = [*serve(items, serving_size=serving_size)]

    expected_full = len(items) // serving_size
    remainder = len(items) % serving_size

    if remainder == 0:
        assert len(dollops) == expected_full
        assert all(len(d) == serving_size for d in dollops)
    else:
        assert len(dollops) == expected_full + 1
        assert all(len(d) == serving_size for d in dollops[:-1])
        assert len(dollops[-1]) == remainder

    assert all(isinstance(d, type(items)) for d in dollops)

    recon = [x for d in dollops for x in d]
    assert len(recon) == len(items)
    assert all(x == y for x, y in zip(recon, items))


@pytest.mark.parametrize('sequence_type', ('list', 'tuple', 'str', 'range', 'bytes', 'bytearray'))
@pytest.mark.parametrize("n_items", (0, 5, 10, 13, 17, 25, 50, 100))
@pytest.mark.parametrize("n_servings", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_sequence_by_n_servings(n_items, n_servings, sequence_type, sequence_creators):

    create_sequence = sequence_creators[sequence_type]

    items = create_sequence(n=n_items)
    dollops = [*serve(items, n_servings=n_servings)]

    assert len(dollops) == n_servings

    max_size = n_items // n_servings + 1
    assert all(len(d) in (max_size - 1, max_size) for d in dollops)
    assert all(isinstance(d, type(items)) for d in dollops)

    recon = [x for d in dollops for x in d]
    assert len(recon) == len(items)
    assert all(x == y for x, y in zip(recon, items))


@pytest.mark.parametrize('non_sequence_type', ('int', 'float', 'none'))
def test_non_sequence_raises_error(non_sequence_type, non_sequences):
    non_sequence = non_sequences[non_sequence_type]
    with pytest.raises(NotImplementedError):
        _ = [*serve(non_sequence, serving_size=10)]
    with pytest.raises(NotImplementedError):
        _ = [*serve(non_sequence, n_servings=10)]
