import io
import pathlib

from typing import Union, Generator


def serve(file: Union[str, pathlib.Path, io.IOBase], serving_size: int, mode='lines') \
                -> Generator[str, None, None]:
    """
    Read a file small dollops at a time.

    :param file: The path or file handle.
    :param serving_size: The max number of lines in each serving.
    :param mode: Either 'lines' or 'chars'/'characters' to read line-by-line or character-by-character.
    :return:
    """

    if mode == 'lines':
        def read_next(h):
            try:
                return next(h)
            except StopIteration:
                return ''

    elif mode in ('characters', 'chars'):
        def read_next(h):
            return h.read(1)

    else:
        raise ValueError('Invalid mode for dollop.file.serve')

    def _serve_handle(h):
        binary = 'b' in h.mode

        finished = False
        while not finished:

            dollop = b'' if binary else ''
            for _ in range(serving_size):
                token = read_next(h)
                if token:
                    dollop += token
                else:
                    finished = True
                    break

            # Check for edge case where there's nothing left.
            if dollop:
                yield dollop

    if isinstance(file, io.IOBase):
        if 'r' not in file.mode:
            raise ValueError('Can only dollop file handles with a read attribute.')
        yield from _serve_handle(file)

    elif isinstance(file, (str, pathlib.Path)):
        with open(file, 'r') as f:
            yield from _serve_handle(f)
