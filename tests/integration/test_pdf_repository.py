import pytest
import fitz
from src.infrastructure.pdf_repository import PyMuPDFRepository

def create_dummy_pdf(path, text="Dummy Content"):
    """Helper to create a valid PDF file."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)
    doc.save(path)
    doc.close()

def test_merge_pdfs_integration(tmp_path):
    """Integration test: Create 2 PDFs, merge them, check page count."""
    # 1. Arrange
    repo = PyMuPDFRepository()
    
    pdf1 = tmp_path / "page1.pdf"
    pdf2 = tmp_path / "page2.pdf"
    output = tmp_path / "merged.pdf"
    
    create_dummy_pdf(pdf1, "Page 1 Content")
    create_dummy_pdf(pdf2, "Page 2 Content")
    
    files = [str(pdf1), str(pdf2)]
    
    # 2. Act
    repo.merge_pdfs(files, str(output))
    
    # 3. Assert
    assert output.exists()
    
    doc = fitz.open(output)
    assert doc.page_count == 2
    
    # Optional: Verify content could be extracted or text is there
    text = ""
    for page in doc:
        text += page.get_text()
        
    assert "Page 1 Content" in text
    assert "Page 2 Content" in text
    doc.close()

from src.core.exceptions import MergeError

def test_merge_pdfs_invalid_input(tmp_path):
    """Test that merging invalid files raises MergeError."""
    repo = PyMuPDFRepository()
    invalid_file = tmp_path / "not_a_pdf.txt"
    invalid_file.write_text("This is not a PDF")
    
    output = tmp_path / "fail.pdf"
    
    with pytest.raises(MergeError, match="Error al procesar el archivo"):
        repo.merge_pdfs([str(invalid_file)], str(output))
