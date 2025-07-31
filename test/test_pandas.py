import pandas as pd
import pytest

from dollop.pandas import serve


@pytest.fixture
def pandas_obj_creators():

    def create_series(n):
        data = [*range(n)]
        series = pd.Series(data)
        series.index = [f'column_{i}' for i in range(n)]
        return series

    def create_dataframe(n):
        n_columns = 10
        data = [[10 ** j + i for j in range(n)] for i in range(n_columns)]
        df = pd.DataFrame(data).T
        df.columns = [f'column_{i}' for i in range(n_columns)]
        return df

    return {
        'series': create_series,
        'df': create_dataframe,
    }


@pytest.fixture
def non_pandas_objs():
    return {
        'list': [1, 2, 3],
        'tuple': (1, 2, 3),
        'int': 10,
        'float': 10.1,
        'none': None,
    }


@pytest.mark.parametrize('pandas_obj_type', ('series', 'df'))
@pytest.mark.parametrize("n_items", (0, 5, 10, 13, 17, 25, 50, 100))
@pytest.mark.parametrize("serving_size", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_pandas_by_serving_size(n_items, serving_size, pandas_obj_type, pandas_obj_creators):

    create_pandas_obj = pandas_obj_creators[pandas_obj_type]

    pandas_obj = create_pandas_obj(n=n_items)
    dollops = [*serve(pandas_obj, serving_size=serving_size)]

    expected_full = len(pandas_obj) // serving_size
    remainder = len(pandas_obj) % serving_size

    if remainder == 0:
        assert len(dollops) == expected_full
        assert all(len(d) == serving_size for d in dollops)
    else:
        assert len(dollops) == expected_full + 1
        assert all(len(d) == serving_size for d in dollops[:-1])
        assert len(dollops[-1]) == remainder

    assert all(isinstance(d, type(pandas_obj)) for d in dollops)

    if len(pandas_obj) > 0:
        recon = pd.concat(dollops)
        assert recon.reset_index(drop=True).equals(pandas_obj.reset_index(drop=True))


@pytest.mark.parametrize('pandas_obj_type', ('series', 'df'))
@pytest.mark.parametrize("n_items", (0, 5, 10, 13, 17, 25, 50, 100))
@pytest.mark.parametrize("n_servings", [1, 2, 3, 5, 10, 21, 25, 27, 100, 200])
def test_serve_pandas_by_n_servings(n_items, n_servings, pandas_obj_type, pandas_obj_creators):

    create_pandas_obj = pandas_obj_creators[pandas_obj_type]

    pandas_obj = create_pandas_obj(n=n_items)
    dollops = [*serve(pandas_obj, n_servings=n_servings)]

    assert len(dollops) == n_servings

    max_size = n_items // n_servings + 1
    assert all(len(d) in (max_size - 1, max_size) for d in dollops)
    assert all(isinstance(d, type(pandas_obj)) for d in dollops)

    if len(pandas_obj) > 0:
        recon = pd.concat(dollops)
        assert recon.reset_index(drop=True).equals(pandas_obj.reset_index(drop=True))


@pytest.mark.parametrize('non_sequence_type', ('list', 'tuple', 'int', 'float', 'none'))
def test_non_pandas_obj_raises_error(non_sequence_type, non_pandas_objs):
    non_sequence = non_pandas_objs[non_sequence_type]
    with pytest.raises(TypeError):
        _ = [*serve(non_sequence, serving_size=10)]
    with pytest.raises(TypeError):
        _ = [*serve(non_sequence, n_servings=10)]
