from typing import Generator, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas # Keep this here for string-based type-checking


def serve(pandas_obj: "pandas.DataFrame | pandas.Series", serving_size: int) -> \
        Generator["pandas.DataFrame | pandas.Series", None, None]:
    """
    Read a Pandas object small chunks at a time.

    :param pandas_obj: The Pandas object.
    :param serving_size: The max number of items in each serving.
    :return: Generator yielding sliced pandas objects.
    """

    cls = pandas_obj.__class__
    is_dataframe = cls.__module__.startswith("pandas.core.frame") and cls.__name__ == "DataFrame"
    is_series = cls.__module__.startswith("pandas.core.series") and cls.__name__ == "Series"

    if not (is_dataframe or is_series):
        raise TypeError(f"Dollop pandas.serve only supports pandas DataFrame or Series")

    for i in range(0, len(pandas_obj), serving_size):
        yield pandas_obj.iloc[i: i + serving_size]

