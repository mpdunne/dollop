import io
import numpy as np
import pandas as pd
import pathlib
import pytest
import torch

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
def file_types():
    return {
        'handle': io.IOBase,
        'pathlib': pathlib.Path,
    }


@pytest.fixture
def pandas_types():
    return {
        'series': pd.Series,
        'df': pd.DataFrame,
    }


@pytest.fixture
def torch_types():
    return {
        'tensor': torch.Tensor,
    }


@pytest.fixture
def numpy_types():
    return {
        'array': np.ndarray,
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


@pytest.mark.parametrize('file_type', ('handle', 'pathlib'))
def test_serve_auto_file_type(file_type, file_types):
    mock_obj = Mock(spec=file_types[file_type])
    with patch('dollop.auto.serve_file') as serve_file:
        serve_file.return_value = iter([None])
        _ = [*serve(mock_obj, serving_size=10)]
        serve_file.assert_called_once()


@pytest.mark.parametrize('file_type', ('handle', 'pathlib'))
def test_serve_auto_file_type_cant_dollop_by_n_servings(file_type, file_types):
    mock_obj = Mock(spec=file_types[file_type])
    with pytest.raises(ValueError):
        _ = [*serve(mock_obj, n_servings=10)]


@pytest.mark.parametrize('pandas_type', ('series', 'df'))
def test_serve_auto_pandas_type(pandas_type, pandas_types):
    mock_obj = Mock(spec=pandas_types[pandas_type])
    with patch('dollop.auto.serve_pandas') as serve_pandas:
        serve_pandas.return_value = iter([None])
        _ = [*serve(mock_obj, serving_size=10)]
        serve_pandas.assert_called_once()


@pytest.mark.parametrize('numpy_type', ('array',))
def test_serve_auto_numpy_types(numpy_type, numpy_types):
    mock_obj = Mock(spec=numpy_types[numpy_type])
    with patch('dollop.auto.serve_numpy') as serve_numpy:
        serve_numpy.return_value = iter([None])
        _ = [*serve(mock_obj, serving_size=10)]
        serve_numpy.assert_called_once()


@pytest.mark.parametrize('torch_type', ('tensor',))
def test_serve_auto_torch_type(torch_type, torch_types):
    mock_obj = Mock(spec=torch_types[torch_type])
    with patch('dollop.auto.serve_torch') as serve_torch:
        serve_torch.return_value = iter([None])
        _ = [*serve(mock_obj, serving_size=10)]
        serve_torch.assert_called_once()


@pytest.mark.parametrize('other_type', ('int', 'float', 'none'))
def test_serve_auto_other_type(other_type, other_types):
    mock_obj = Mock(spec=other_types[other_type])
    with patch('dollop.auto.serve_sequence') as serve_sequence:
        with pytest.raises(NotImplementedError):
            _ = [*serve(mock_obj, serving_size=10)]
