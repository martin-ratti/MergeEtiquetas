import pytest
import os
import shutil
from pathlib import Path

@pytest.fixture
def temp_input_dir(tmp_path):
    """Creates a temporary input directory with some dummy files."""
    d = tmp_path / "_ETIQUETAS_PDFS"
    d.mkdir()
    return d

@pytest.fixture
def temp_output_dir(tmp_path):
    """Creates a temporary output directory."""
    d = tmp_path / "_SALIDA"
    d.mkdir()
    return d

@pytest.fixture
def valid_config():
    """Returns a valid configuration dictionary."""
    return {
        'EMAIL_EMISOR': 'test@example.com',
        'APP_PASSWORD': 'password',
        'EMAIL_RECEPTOR': 'receiver@example.com',
        'ASUNTO': 'Test Subject'
    }
