import pytest

from unittest.mock import Mock, patch

from dollop.auto import serve as serve


@pytest.fixture
def sequence_types():
    return {
        'list': list,
        'tuple': tuple,
        'str': str,
        'range': range,
        'bytes': bytes,
        'bytearray': bytearray,
    }


@pytest.fixture
def other_types():
    return {
        'int': int,
        'float': float,
        'none': None,
    }


@pytest.mark.parametrize('sequence_type', ('list', 'tuple', 'str', 'range', 'bytes', 'bytearray'))
def test_serve_auto_sequence_type(sequence_type, sequence_types):
    mock_obj = Mock(spec=sequence_types[sequence_type])
    with patch('dollop.auto.serve_sequence') as serve_sequence:
        serve_sequence.return_value = iter([None])
        _ = [*serve(mock_obj, serving_size=10)]
        serve_sequence.assert_called_once()


@pytest.mark.parametrize('other_type', ('int', 'float', 'none'))
def test_serve_auto_other_type(other_type, other_types):
    mock_obj = Mock(spec=other_types[other_type])
    with patch('dollop.auto.serve_sequence') as serve_sequence:
        with pytest.raises(NotImplementedError):
            _ = [*serve(mock_obj, serving_size=10)]
