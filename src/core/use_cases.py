# src/core/use_cases.py
from typing import List, Dict
from src.core.interfaces import IPdfRepository, IEmailService # <--- MODIFICADO
from pathlib import Path

def merge_pdfs_use_case(
    pdf_files: List[str], 
    output_path: str, 
    pdf_repository: IPdfRepository
) -> None:
    """
    Caso de uso para fusionar múltiples archivos PDF en uno solo.
    
    Args:
        pdf_files (List[str]): La lista de rutas de archivo a fusionar.
        output_path (str): La ruta del archivo de salida.
        pdf_repository (IPdfRepository): Una implementación de IPdfRepository.
    """
    if not pdf_files:
        raise ValueError("La lista de archivos PDF no puede estar vacía.")
        
    if not output_path.lower().endswith('.pdf'):
        raise ValueError("La ruta de salida debe ser un archivo .pdf")

    pdf_repository.merge_pdfs(pdf_file_paths=pdf_files, output_path=output_path)


# --- NUEVO CASO DE USO ---
def send_pdf_by_email_use_case(
    config: Dict[str, str],
    pdf_path: str,
    email_service: IEmailService
) -> None:
    """
    Caso de uso para enviar un PDF por email.
    
    Contiene la lógica de negocio para validar la solicitud antes
    de pasarla a la capa de infraestructura.

    Args:
        config (Dict[str, str]): Diccionario de configuración del email.
        pdf_path (str): Ruta al PDF que se debe adjuntar.
        email_service (IEmailService): Una implementación de IEmailService.
        
    Raises:
        ValueError: Si la configuración está incompleta o el archivo no existe.
    """
    # 1. Validar que el archivo PDF exista
    if not Path(pdf_path).exists():
        raise ValueError(f"El archivo PDF no se encontró en: {pdf_path}")
        
    # 2. Validar que la configuración esencial esté presente
    required_keys = ['EMAIL_EMISOR', 'APP_PASSWORD', 'EMAIL_RECEPTOR', 'ASUNTO']
    if not all(key in config and config[key] for key in required_keys):
        raise ValueError("La configuración de email (config.ini) está incompleta.")

    # 3. Delegar el trabajo técnico al servicio de infraestructura
    email_service.send_email_with_attachment(config, pdf_path)