import io
import pathlib
import pandas as pd

from typing import Union, Generator

PandasType = Union[pd.DataFrame, pd.Series]


def serve(pandas_obj: PandasType, serving_size: int) -> Generator[PandasType, None, None]:
    """
    Read a Pandas object small chunks at a time.

    :param pandas_obj: The Pandas object.
    :param serving_size: The max number of items in each serving.
    :return:
    """
    if isinstance(pandas_obj, (pd.DataFrame, pd.Series)):
        for i in range(0, len(pandas_obj), serving_size):
            yield pandas_obj.iloc[i: i + serving_size]
    else:
        raise NotImplementedError('Dollop pandas.serve only supports objects of DataFrame or Series types.')
