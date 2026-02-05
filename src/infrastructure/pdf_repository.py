# src/infrastructure/pdf_repository.py
import fitz  # PyMuPDF
from typing import List
from src.core.interfaces import IPdfRepository

from src.core.exceptions import MergeError

class PyMuPDFRepository(IPdfRepository):
    """
    Implementación concreta de IPdfRepository usando la librería PyMuPDF.
    
    Esta capa SÍ conoce los detalles de las librerías externas (Pilar 1).
    """

    def merge_pdfs(self, pdf_file_paths: List[str], output_path: str, on_progress: callable = None) -> None:
        """
        Fusiona PDFs usando PyMuPDF (fitz) por su alta eficiencia.
        
        Args:
            pdf_file_paths (List[str]): Lista de rutas a los archivos PDF.
            output_path (str): Ruta al archivo PDF de salida.
            on_progress (callable, optional): Callback (actual, total).
            
        Raises:
            MergeError: Si ocurre un error al procesar o guardar un PDF.
        """
        result_pdf = fitz.open()
        total_files = len(pdf_file_paths)

        try:
            for i, pdf_path in enumerate(pdf_file_paths):
                if on_progress:
                    on_progress(i, total_files)
                try:
                    # Usamos 'with' para asegurar el cierre del descriptor del archivo
                    with fitz.open(pdf_path) as pdf_doc:
                        result_pdf.insert_pdf(pdf_doc)
                except Exception as e:
                    # El 'finally' general se encargará de cerrar result_pdf
                    raise MergeError(
                        f"Error al procesar el archivo '{pdf_path}': {e}"
                    )
            
            if on_progress:
                on_progress(total_files, total_files)

            try:
                result_pdf.save(output_path)
            except Exception as e:
                raise MergeError(
                    f"Error al guardar el archivo de salida '{output_path}': {e}"
                )
        finally:
            # Aseguramos que siempre se liberen los recursos de memoria
            result_pdf.close()