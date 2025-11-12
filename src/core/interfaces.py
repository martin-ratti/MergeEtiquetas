# src/core/interfaces.py
from abc import ABC, abstractmethod
from typing import List

class IPdfRepository(ABC):
    """
    Define la interfaz (el "contrato") para las operaciones de PDF.
    
    La capa 'core' depende de esta abstracción, no de una implementación
    concreta (Pilar 1: Inversión de Dependencias).
    """

    @abstractmethod
    def merge_pdfs(self, pdf_file_paths: List[str], output_path: str) -> None:
        """
        Fusiona una lista de archivos PDF en un único archivo de salida.

        Args:
            pdf_file_paths (List[str]): Lista de rutas a los archivos PDF de entrada.
            output_path (str): Ruta al archivo PDF de salida.
        """
        pass