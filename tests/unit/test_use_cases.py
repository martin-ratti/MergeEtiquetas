import pytest
from unittest.mock import Mock, MagicMock
from src.core.use_cases import merge_pdfs_use_case, send_pdf_by_email_use_case
from src.core.interfaces import IPdfRepository, IEmailService

def test_merge_pdfs_use_case_empty_list():
    """Test that merging an empty list raises ValueError."""
    repo = Mock(spec=IPdfRepository)
    with pytest.raises(ValueError, match="La lista de archivos PDF no puede estar vacía"):
        merge_pdfs_use_case([], "out.pdf", repo)

def test_merge_pdfs_use_case_invalid_extension():
    """Test that output path without .pdf extension raises ValueError."""
    repo = Mock(spec=IPdfRepository)
    with pytest.raises(ValueError, match="La ruta de salida debe ser un archivo .pdf"):
        merge_pdfs_use_case(["a.pdf"], "out.txt", repo)

def test_merge_pdfs_success():
    """Test successful call to repository."""
    repo = Mock(spec=IPdfRepository)
    files = ["a.pdf", "b.pdf"]
    output = "out.pdf"
    
    merge_pdfs_use_case(files, output, repo)
    
    repo.merge_pdfs.assert_called_once_with(
        pdf_file_paths=files, 
        output_path=output, 
        on_progress=None
    )

def test_send_email_use_case_no_pdf():
    """Test that sending a non-existent PDF raises ValueError."""
    service = Mock(spec=IEmailService)
    config = {}
    with pytest.raises(ValueError, match="El archivo PDF no se encontró"):
        send_pdf_by_email_use_case(config, "non_existent.pdf", service)

def test_send_email_use_case_invalid_config(tmp_path):
    """Test that missing config keys raises ValueError."""
    # Create dummy pdf
    pdf = tmp_path / "test.pdf"
    pdf.touch()
    
    service = Mock(spec=IEmailService)
    config = {'EMAIL_EMISOR': 'me'} # Missing others
    
    with pytest.raises(ValueError, match="La configuración de email .* está incompleta"):
        send_pdf_by_email_use_case(config, str(pdf), service)

def test_send_email_success(tmp_path, valid_config):
    """Test successful email sending delegation."""
    pdf = tmp_path / "test.pdf"
    pdf.touch()
    
    service = Mock(spec=IEmailService)
    
    send_pdf_by_email_use_case(valid_config, str(pdf), service)
    
    service.send_email_with_attachment.assert_called_once_with(valid_config, str(pdf))
