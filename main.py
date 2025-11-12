# main.py
import os
import sys
from pathlib import Path
from src.interface.app_gui import App
from src.core.use_cases import merge_pdfs_use_case
from src.infrastructure.pdf_repository import PyMuPDFRepository

# --- Definición de Rutas Constantes ---

def get_project_root() -> Path:
    """
    Obtiene la raíz del proyecto, donde las carpetas de usuario
    (_ETIQUETAS_PDFS, _SALIDA) deben estar.
    """
    if getattr(sys, 'frozen', False):
        # Modo empaquetado (.exe): la raíz es la carpeta del .exe
        return Path(sys.executable).resolve().parent
    else:
        # Modo desarrollo (python main.py): la raíz es la carpeta del script
        return Path(__file__).resolve().parent

def get_asset_path(file_name: str) -> Path:
    """
    Obtiene la ruta correcta a un activo (como logo.png)
    que está empaquetado DENTRO del .exe.
    """
    if getattr(sys, 'frozen', False):
        # Modo empaquetado: el activo está en el dir temporal _MEIPASS
        base_path = Path(sys._MEIPASS)
    else:
        # Modo desarrollo: el activo está junto a main.py
        base_path = Path(__file__).resolve().parent
        
    return base_path / file_name

# Definir rutas globales usando las funciones
ROOT_DIR = get_project_root()
INPUT_DIR = ROOT_DIR / "_ETIQUETAS_PDFS"
OUTPUT_DIR = ROOT_DIR / "_SALIDA"
LOGO_FILE = get_asset_path("logo.png")


def main():
    """
    Punto de entrada principal de la aplicación.
    Configura las carpetas, inyecta las dependencias e inicia la GUI.
    """
    
    # 1. Asegurar que las carpetas de E/S existan
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Crear una categoría de ejemplo si el directorio está vacío (mejora de UX)
    if not any(INPUT_DIR.iterdir()):
        (INPUT_DIR / "01_Ejemplo_Categoria").mkdir(exist_ok=True)
        print(f"Carpetas creadas. Agrega tus PDFs en: {INPUT_DIR}")

    # 2. Inyección de Dependencias (Clean Architecture)
    # Instanciar la implementación concreta
    pdf_repository = PyMuPDFRepository()
    
    # Crear una función wrapper del caso de uso para pasar a la GUI
    def merge_use_case_func(files: list[str], output: str):
        """Función wrapper para aislar el núcleo de la GUI."""
        merge_pdfs_use_case(
            pdf_files=files, 
            output_path=output, 
            pdf_repository=pdf_repository
        )

    # 3. Iniciar la Aplicación (Capa de Interface)
    app = App(
        merge_use_case=merge_use_case_func,
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        logo_file=LOGO_FILE
    )
    app.mainloop()

if __name__ == "__main__":
    main()