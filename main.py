# main.py
import os
import sys
from pathlib import Path
from src.interface.app_gui import App
# --- MODIFICADO ---
from src.core.use_cases import merge_pdfs_use_case, send_pdf_by_email_use_case
from src.infrastructure.pdf_repository import PyMuPDFRepository
from src.infrastructure.smtp_email_service import SMTPEmailService
# --- FIN MODIFICADO ---


def get_project_root() -> Path:
    """
    Obtiene la raíz del proyecto, donde las carpetas de usuario
    (_ETIQUETAS_PDFS, _SALIDA, config.ini) deben estar.
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    else:
        return Path(__file__).resolve().parent

def get_asset_path(file_name: str) -> Path:
    """
    Obtiene la ruta correcta a un activo (como logo.png)
    que está empaquetado DENTRO del .exe.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
        
    return base_path / file_name

# Definir rutas globales
ROOT_DIR = get_project_root()
INPUT_DIR = ROOT_DIR / "_ETIQUETAS_PDFS"
OUTPUT_DIR = ROOT_DIR / "_SALIDA"
LOGO_FILE = get_asset_path("logo.png")
# --- NUEVA RUTA ---
CONFIG_FILE = ROOT_DIR / "config.ini"


def main():
    """
    Punto de entrada principal de la aplicación.
    Configura las carpetas, inyecta las dependencias e inicia la GUI.
    """
    
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    if not any(INPUT_DIR.iterdir()):
        (INPUT_DIR / "01_Ejemplo_Categoria").mkdir(exist_ok=True)
        print(f"Carpetas creadas. Agrega tus PDFs en: {INPUT_DIR}")

    # 2. Inyección de Dependencias
    
    # Repositorio de PDF
    pdf_repository = PyMuPDFRepository()
    def merge_use_case_func(files: list[str], output: str, on_progress: callable = None):
        merge_pdfs_use_case(
            pdf_files=files, 
            output_path=output, 
            pdf_repository=pdf_repository,
            on_progress=on_progress
        )

    # --- NUEVO: Servicio de Email ---
    email_service = SMTPEmailService()
    def send_email_use_case_func(config: dict, pdf_path: str):
        send_pdf_by_email_use_case(
            config=config,
            pdf_path=pdf_path,
            email_service=email_service
        )
    # --- FIN NUEVO ---

    # 3. Iniciar la Aplicación (Interface)
    app = App(
        merge_use_case=merge_use_case_func,
        send_email_use_case=send_email_use_case_func, # <--- MODIFICADO
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        logo_file=LOGO_FILE,
        config_file=CONFIG_FILE # <--- NUEVO
    )
    app.mainloop()

if __name__ == "__main__":
    main()