from typing import Any, Generator, Sequence
from collections.abc import Sequence as SequenceType

from ._utils import calculate_slices


def serve(items: Sequence[Any], serving_size: int = None, n_servings: int = None) -> Generator[Sequence[Any], None, None]:
    """
    Split a sequence of items into a number of smaller dollops.

    :param items: The original sequence of items.
    :param serving_size: The number of items per dollop. Mutually exclusive with n_servings.
    :param n_servings: The number of dollops, of roughly equal size. Mutually exclusive with serving_size.
    :return: Generator yielding sliced subsequences.
    """

    if not isinstance(items, SequenceType):
        raise NotImplementedError('Dollop sequence.serve only supports objects of Sequence type.')

    slices = calculate_slices(total=len(items), serving_size=serving_size, n_servings=n_servings)

    for slc in slices:
        yield items[slc]
