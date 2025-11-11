# src/core/use_cases.py
from typing import List
from src.core.interfaces import IPdfRepository

def merge_pdfs_use_case(
    pdf_files: List[str], 
    output_path: str, 
    pdf_repository: IPdfRepository
) -> None:
    """
    Caso de uso para fusionar múltiples archivos PDF en uno solo.

    Esta función contiene la lógica de negocio pura:
    1. Valida la entrada.
    2. Orquesta la fusión llamando al repositorio.

    Args:
        pdf_files (List[str]): La lista de rutas de archivo a fusionar.
        output_path (str): La ruta del archivo de salida.
        pdf_repository (IPdfRepository): La implementación concreta de 
                                         la infraestructura para manejar PDFs.

    Raises:
        ValueError: Si no se proporcionan archivos de entrada o la salida
                    no es un .pdf.
    """
    if not pdf_files:
        raise ValueError("La lista de archivos PDF no puede estar vacía.")
        
    if not output_path.lower().endswith('.pdf'):
        raise ValueError("La ruta de salida debe ser un archivo .pdf")

    # La lógica de negocio es simplemente llamar a la infraestructura
    # para que haga el trabajo (Pilar 1: Regla de Dependencia).
    pdf_repository.merge_pdfs(pdf_file_paths=pdf_files, output_path=output_path)