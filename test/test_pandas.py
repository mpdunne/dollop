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
def test_pandas_obj_works(n_items, serving_size, expected_n_full_servings, expected_remainder,
                      pandas_obj_type, pandas_obj_creators):

    create_pandas_obj = pandas_obj_creators[pandas_obj_type]

    pandas_obj = create_pandas_obj(n=n_items)
    dollops = [*serve(pandas_obj, serving_size=serving_size)]

    if expected_remainder == 0:
        assert len(dollops) == expected_n_full_servings
        assert all([len(d) == serving_size for d in dollops])
    else:
        assert len(dollops) == expected_n_full_servings + 1
        assert all([len(d) == serving_size for d in dollops[:-1]])
        assert len(dollops[-1]) == expected_remainder

    if n_items != 0:
        assert (pd.concat(dollops) == pandas_obj).all().all()
        assert all([type(serving) == type(pandas_obj) for serving in dollops])


@pytest.mark.parametrize('non_sequence_type', ('list', 'tuple', 'int', 'float', 'none'))
def test_non_pandas_obj_raises_error(non_sequence_type, non_pandas_objs):
    non_sequence = non_pandas_objs[non_sequence_type]
    with pytest.raises(TypeError):
        _ = [*serve(non_sequence, serving_size=10)]
