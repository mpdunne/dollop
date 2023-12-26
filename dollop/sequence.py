from typing import Any, Generator, Sequence
from collections.abc import Sequence as SequenceType


def serve(items: Sequence[Any], serving_size: int) -> Generator[Sequence[Any], None, None]:
    """
    Split a sequence of items into a number of smaller sequences, with max serving_size items in each.

    :param items: The original sequence of items.
    :param serving_size: The max number of items in each outputted subsequence.
    :return:
    """

    if not isinstance(items, SequenceType):
        raise NotImplementedError('Dollop sequence.serve only supports objects of Sequence type.')

    for i in range(0, len(items), serving_size):
        yield items[i: i + serving_size]
