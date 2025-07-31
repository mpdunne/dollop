from typing import Generator, TYPE_CHECKING

from ._utils import calculate_slices

if TYPE_CHECKING:
    import pandas # Keep this here for string-based type-checking


def serve(pandas_obj: "pandas.DataFrame | pandas.Series", serving_size: int = None, n_servings: int = None) -> \
        Generator["pandas.DataFrame | pandas.Series", None, None]:
    """
    Read a Pandas object small chunks at a time.

    :param pandas_obj: The Pandas object.
    :param serving_size: The size of each slice. Mutually exclusive with n_servings.
    :param n_servings: The size of each slice. Mutually exclusive with serving_size.
    :return: Generator yielding sliced pandas objects.
    """

    cls = pandas_obj.__class__
    is_dataframe = cls.__module__.startswith("pandas.core.frame") and cls.__name__ == "DataFrame"
    is_series = cls.__module__.startswith("pandas.core.series") and cls.__name__ == "Series"

    if not (is_dataframe or is_series):
        raise TypeError(f"Dollop pandas.serve only supports pandas DataFrame or Series")

    slices = calculate_slices(total=len(pandas_obj), serving_size=serving_size, n_servings=n_servings)

    for slc in slices:
        yield pandas_obj.iloc[slc]

