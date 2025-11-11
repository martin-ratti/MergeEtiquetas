# main.py
import os
import sys  # Importamos 'sys' para detectar el modo de ejecución
from pathlib import Path
from src.interface.app_gui import App
from src.core.use_cases import merge_pdfs_use_case
from src.infrastructure.pdf_repository import PyMuPDFRepository

# --- Definición de Rutas Constantes (Pilar 3 - CORREGIDO) ---

def get_project_root() -> Path:
    """
    Obtiene la raíz del proyecto, donde las carpetas de usuario
    (_ETIQUETAS_PDFS, _SALIDA) deben estar.
    """
    if getattr(sys, 'frozen', False):
        # Estamos en un .exe de PyInstaller.
        # La raíz del proyecto ES la carpeta donde está el .exe.
        # (HEMOS QUITADO EL .parent extra)
        return Path(sys.executable).resolve().parent
    else:
        # Estamos en modo de desarrollo (python main.py).
        # La raíz es la carpeta donde está main.py.
        return Path(__file__).resolve().parent

def get_asset_path(file_name: str) -> Path:
    """
    Obtiene la ruta correcta a un activo (como logo.png)
    que está empaquetado CON el .exe.
    (Esta función ya era correcta y no cambia)
    """
    if getattr(sys, 'frozen', False):
        # Estamos en un .exe. El activo está en el dir temporal _MEIPASS.
        base_path = Path(sys._MEIPASS)
    else:
        # Estamos en desarrollo. El activo está junto a main.py.
        base_path = Path(__file__).resolve().parent
        
    return base_path / file_name

def get_asset_path(file_name: str) -> Path:
    """
    Obtiene la ruta correcta a un activo (como logo.png)
    que está empaquetado CON el .exe.
    """
    if getattr(sys, 'frozen', False):
        # Estamos en un .exe. El activo está en el dir temporal _MEIPASS.
        base_path = Path(sys._MEIPASS)
    else:
        # Estamos en desarrollo. El activo está junto a main.py.
        base_path = Path(__file__).resolve().parent
        
    return base_path / file_name

# Definir rutas usando las nuevas funciones
ROOT_DIR = get_project_root()
INPUT_DIR = ROOT_DIR / "_ETIQUETAS_PDFS"
OUTPUT_DIR = ROOT_DIR / "_SALIDA"

# El logo es un 'asset', por lo que usa la otra función
LOGO_FILE = get_asset_path("logo.png") # Asumiendo que se llama logo.png


def main():
    """
    Punto de entrada principal de la aplicación.
    Configura las carpetas, inyecta las dependencias e inicia la GUI.
    """
    
    # 1. Asegurar que las carpetas existan (UX y Robustez)
    # Esto ahora las creará en la raíz del proyecto, no en 'dist/'.
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # (Opcional) Crear una categoría de ejemplo
    if not any(INPUT_DIR.iterdir()):
        (INPUT_DIR / "01_Ejemplo_Categoria").mkdir(exist_ok=True)
        print(f"Carpetas creadas. Agrega tus PDFs en: {INPUT_DIR}")

    # 2. Inyección de Dependencias (Clean Architecture)
    pdf_repository = PyMuPDFRepository()
    
    def merge_use_case_func(files: list[str], output: str):
        """Función wrapper para pasar al núcleo de la GUI."""
        merge_pdfs_use_case(
            pdf_files=files, 
            output_path=output, 
            pdf_repository=pdf_repository
        )

    # 3. Iniciar la Aplicación (Interface)
    app = App(
        merge_use_case=merge_use_case_func,
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        logo_file=LOGO_FILE  # Pasamos la ruta de asset corregida
    )
    app.mainloop()

if __name__ == "__main__":
    main()