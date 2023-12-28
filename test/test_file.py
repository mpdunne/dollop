import pytest
import re

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from dollop.file import serve


@pytest.fixture
def non_empty_file():

    content = '\"Fog\"\n' + \
              'by Carl Sandburg\n' + \
              '\n' + \
              'The fog comes\n' + \
              'on little cat feet.\n' + \
              '\n' + \
              'It sits looking\n' + \
              'over harbor and city\n' + \
              'on silent haunches\n' + \
              'and then moves on.'

    with TemporaryDirectory() as td:
        temp_file = f'{td}/content.txt'
        with open(temp_file, 'w') as f:
            f.write(content)
        yield temp_file


@pytest.fixture
def empty_file():
    with TemporaryDirectory() as td:
        temp_file = f'{td}/empty.txt'
        with open(temp_file, 'w') as f:
            pass
        yield temp_file


@pytest.fixture
def file_obj_creators():

    def create_string(file_path):
        return file_path

    def create_pathlib(file_path):
        return Path(file_path)

    def create_handle(file_path):
        return open(file_path, 'r')

    def create_handle_binary(file_path):
        return open(file_path, 'rb')

    return {
        'string': create_string,
        'pathlib': create_pathlib,
        'handle': create_handle,
        'handle_binary': create_handle_binary,
    }


@pytest.mark.parametrize('mode', ('characters', 'lines'))
@pytest.mark.parametrize('file_obj_type', ('string', 'pathlib', 'handle', 'handle_binary'))
def test_serve_empty_file(mode, file_obj_type, file_obj_creators, empty_file):
    create_file_obj = file_obj_creators[file_obj_type]
    file_obj = create_file_obj(empty_file)
    dollops = [*serve(file_obj, serving_size=10, mode=mode)]
    assert len(dollops) == 0


@pytest.mark.parametrize('file_obj_type', ('string', 'pathlib', 'handle', 'handle_binary'))
@pytest.mark.parametrize(
    'mode,serving_size,expected_n_full_servings,expected_remainder',
    (
            ('lines', 10, 1, 0),  # everything in one serving
            ('lines', 5, 2, 0),  # split, no remainder
            ('lines', 3, 3, 1),  # split, remainder
            ('lines', 20, 0, 10),  # no full servings, remainder
            ('characters', 133, 1, 0),  # everything in one serving
            ('characters', 19, 7, 0),  # split, no remainder
            ('characters', 20, 6, 13),  # split, remainder
            ('characters', 200, 0, 133),  # no full servings, remainder
    )
)
def test_serve_nonempty_file(mode, file_obj_type,
                             serving_size, expected_n_full_servings, expected_remainder,
                             file_obj_creators, non_empty_file):
    create_file_obj = file_obj_creators[file_obj_type]
    file_obj = create_file_obj(non_empty_file)
    dollops = [*serve(file_obj, serving_size=serving_size, mode=mode)]

    # Count the total number of lines
    subdollops = [d.splitlines() for d in dollops] if mode == 'lines' else dollops

    if expected_remainder == 0:
        assert len(dollops) == expected_n_full_servings
        assert all([len(d) == serving_size for d in subdollops])

    else:
        assert len(dollops) == expected_n_full_servings + 1
        assert all([len(d) == serving_size for d in subdollops[:-1]])
        assert len(subdollops[-1]) == expected_remainder


def test_unknown_mode_raises_error():
    with pytest.raises(ValueError):
        _ = [*serve('file.txt', serving_size=1, mode='words')]


def test_write_handle_raises_error():
    with NamedTemporaryFile() as tf:
        with pytest.raises(ValueError):
            _ = [*serve(open(tf.name, 'w'), serving_size=1)]


def test_nonexistent_file_raises_error():
    with TemporaryDirectory() as td:
        with pytest.raises(FileNotFoundError):
            _ = [*serve(f'{td}/file.txt', serving_size=1)]
