import pytest

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from dollop.file import serve


def helper_create_and_serve_file_obj(content, file_obj_type, mode, serving_size):

    with TemporaryDirectory() as td:

        file_path = f'{td}/content.txt'
        with open(file_path, 'w') as f:
            f.write(content)

        if file_obj_type == 'string':
            file_obj = file_path
        elif file_obj_type == 'pathlib':
            file_obj = Path(file_path)
        elif file_obj_type == 'handle':
            file_obj = open(file_path, 'r')
        elif file_obj_type == 'handle_binary':
            file_obj = open(file_path, 'rb')
        else:
            raise ValueError('Invalid file_obj_type.')

        dollops = [*serve(file_obj, serving_size=serving_size, mode=mode)]
        return dollops


def helper_test_served_file_obj(content, dollops, mode, serving_size,
                                expected_n_full_servings, expected_remainder, binary):

    subdollops = [d.splitlines() for d in dollops] if mode == 'lines' else dollops

    if expected_remainder == 0:
        assert len(dollops) == expected_n_full_servings
        assert all([len(d) == serving_size for d in subdollops])

    else:
        assert len(dollops) == expected_n_full_servings + 1
        assert all([len(d) == serving_size for d in subdollops[:-1]])
        assert len(subdollops[-1]) == expected_remainder

    if binary:
        assert all([type(d) == bytes for d in dollops])
        undolloped = ''.join([d.decode() for d in dollops])
    else:
        assert all([type(d) == str for d in dollops])
        undolloped = ''.join(dollops)

    assert undolloped.splitlines() == content.splitlines()


@pytest.mark.parametrize('mode', ('characters', 'lines'))
@pytest.mark.parametrize('file_obj_type', ('string', 'pathlib', 'handle', 'handle_binary'))
def test_serve_empty_file(mode, file_obj_type):
    content = ''
    dollops = helper_create_and_serve_file_obj(content, file_obj_type, mode, serving_size=10)
    assert len(dollops) == 0


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
@pytest.mark.parametrize('file_obj_type', ('string', 'pathlib', 'handle', 'handle_binary'))
def test_serve_nonempty_file_poem(mode, file_obj_type,
                                  serving_size, expected_n_full_servings, expected_remainder):
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

    dollops = helper_create_and_serve_file_obj(content, file_obj_type, mode, serving_size)
    helper_test_served_file_obj(content, dollops, mode, serving_size,
                                expected_n_full_servings, expected_remainder, binary=(file_obj_type=='handle_binary'))


@pytest.mark.parametrize(
    'mode,serving_size,expected_n_full_servings,expected_remainder',
    (
            ('lines', 10, 1, 0),  # everything in one serving
            ('lines', 5, 2, 0),  # split, no remainder
            ('lines', 3, 3, 1),  # split, remainder
            ('lines', 20, 0, 10),  # no full servings, remainder
            ('characters', 40, 1, 0),  # everything in one serving
            ('characters', 20, 2, 0),  # split, no remainder
            ('characters', 17, 2, 6),  # split, remainder
            ('characters', 50, 0, 40),  # no full servings, remainder
    )
)
@pytest.mark.parametrize('file_obj_type', ('string', 'pathlib', 'handle', 'handle_binary'))
def test_serve_nonempty_file_blank_space(mode, file_obj_type,
                                         serving_size, expected_n_full_servings, expected_remainder):
    content = '\n' + \
              '\n' + \
              '\n' + \
              'nice to\n' + \
              '\n' + \
              'meet you\n' + \
              '\n' + \
              '\n' + \
              '\n' + \
              'where you been?\n'

    dollops = helper_create_and_serve_file_obj(content, file_obj_type, mode, serving_size)
    helper_test_served_file_obj(content, dollops, mode, serving_size,
                                expected_n_full_servings, expected_remainder, binary=(file_obj_type=='handle_binary'))


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

