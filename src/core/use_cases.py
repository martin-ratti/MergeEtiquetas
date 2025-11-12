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

    Esta función contiene la lógica de negocio pura y es agnóstica
    a la GUI o a las librerías externas.

    Args:
        pdf_files (List[str]): La lista de rutas de archivo a fusionar.
        output_path (str): La ruta del archivo de salida.
        pdf_repository (IPdfRepository): Una implementación del contrato
                                         IPdfRepository.
    Raises:
        ValueError: Si no se proporcionan archivos de entrada o la salida
                    no es un .pdf.
    """
    if not pdf_files:
        raise ValueError("La lista de archivos PDF no puede estar vacía.")
        
    if not output_path.lower().endswith('.pdf'):
        raise ValueError("La ruta de salida debe ser un archivo .pdf")

    # La lógica de negocio delega el trabajo técnico al repositorio
    pdf_repository.merge_pdfs(pdf_file_paths=pdf_files, output_path=output_path)