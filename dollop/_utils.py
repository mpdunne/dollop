from typing import List


def validate_serving_args(serving_size=None, n_servings=None) -> None:
    """
    Check the type, value, and mutual exclusivity of serving_size and n_servings.
    Raise an error if something is wrong, otherwise move on.

    :param serving_size: The serving size.
    :param n_servings: The number of servings
    """

    if (serving_size is None) == (n_servings is None):
        raise ValueError("Exactly one of `serving_size` or `n_servings` must be specified.")

    val = serving_size if serving_size is not None else n_servings
    if not isinstance(val, int) or val <= 0:
        raise TypeError("`serving_size` or `n_servings` must be an integer > 0.")


def calculate_slices(total: int, serving_size: int = None, n_servings: int = None) -> List[slice]:
    """
    Return a sequence of slice indices for a known total number of items, using either a consistent
    serving size (consistent except for the last dollop) or a set number of servings.

    :param total: Total number of items.
    :param serving_size: Desired maximum size per dollop. Mutually exclusive with n_servings.
    :param n_servings: Desired number of dollops. Mutually exclusive with serving_size.
    :return: List of (start, stop) index tuples.
    """
    if (serving_size is None) == (n_servings is None):
        raise ValueError("Exactly one of serving_size or n_servings must be specified.")

    if total < 0:
        raise ValueError("Total length must be non-negative.")

    if serving_size is not None:

        if not isinstance(serving_size, int) or serving_size <= 0:
            raise ValueError("serving_size must be a positive integer.")

        slices = [slice(i, min(i + serving_size, total)) for i in range(0, total, serving_size)]

    else:

        if not isinstance(n_servings, int) or n_servings <= 0:
            raise ValueError("n_servings must be a positive integer.")

        # Calculate sizes to divide total into `n_servings` chunks as evenly as possible
        base = total // n_servings
        remainder = total % n_servings

        slices = []
        start = 0
        for i in range(n_servings):
            dollop_size = base + 1 if i < remainder else base
            stop = start + dollop_size
            slices.append(slice(start, stop))
            start = stop

    return slices
