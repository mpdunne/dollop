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
@pytest.mark.parametrize(
    'n_items,serving_size,expected_n_full_servings,expected_remainder',
    (
            (0, 10, 0, 0),  # empty
            (10, 10, 1, 0),  # everything in one serving
            (10, 5, 2, 0),  # split, no remainder
            (10, 3, 3, 1),  # split, remainder
            (10, 15, 0, 10),  # no full servings, remainder
    )
)
def test_sequence_works(n_items, serving_size, expected_n_full_servings, expected_remainder,
                        sequence_type, sequence_creators):
    create_sequence = sequence_creators[sequence_type]

    items = create_sequence(n=n_items)
    dollops = [*serve(items, serving_size=serving_size)]

    if expected_remainder == 0:
        assert len(dollops) == expected_n_full_servings
        assert all([len(d) == serving_size for d in dollops])
    else:
        assert len(dollops) == expected_n_full_servings + 1
        assert all([len(d) == serving_size for d in dollops[:-1]])
        assert len(dollops[-1]) == expected_remainder

    expected_items = [x for c in dollops for x in c]
    assert all(x == y for x, y in zip(expected_items, items))

    assert all([type(serving) == type(items) for serving in dollops])


@pytest.mark.parametrize('non_sequence_type', ('int', 'float', 'none'))
def test_non_sequence_raises_error(non_sequence_type, non_sequences):
    non_sequence = non_sequences[non_sequence_type]
    with pytest.raises(NotImplementedError):
        _ = [*serve(non_sequence, serving_size=10)]
    with pytest.raises(NotImplementedError):
        _ = [*serve(non_sequence, n_servings=10)]
