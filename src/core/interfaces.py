# src/core/interfaces.py
from abc import ABC, abstractmethod
from typing import List, Dict

class IPdfRepository(ABC):
    """
    Define la interfaz (el "contrato") para las operaciones de PDF.
    """
    @abstractmethod
    def merge_pdfs(self, pdf_file_paths: List[str], output_path: str, on_progress: callable = None) -> None:
        """
        Fusiona una lista de archivos PDF en un único archivo de salida.
        
        Args:
            pdf_file_paths (List[str]): Lista de rutas a los archivos PDF de entrada.
            output_path (str): Ruta al archivo PDF de salida.
            on_progress (callable, optional): Callback que recibe (actual, total) para reportar progreso.
        """
        pass

# --- NUEVA INTERFAZ ---
class IEmailService(ABC):
    """
    Define la interfaz (el "contrato") para el servicio de envío de email.
    """
    @abstractmethod
    def send_email_with_attachment(self, config: Dict[str, str], file_path: str) -> None:
        """
        Envía un email con un archivo adjunto.

        Args:
            config (Dict[str, str]): Un diccionario que contiene
                'EMAIL_EMISOR', 'APP_PASSWORD', 'EMAIL_RECEPTOR', 'ASUNTO'.
            file_path (str): Ruta al archivo que se debe adjuntar.
        
        Raises:
            ValueError: Si la configuración es inválida.
            RuntimeError: Si falla la conexión o la autenticación.
        """
        pass