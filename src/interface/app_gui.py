# src/interface/app_gui.py
import customtkinter
from PIL import Image
from pathlib import Path
from typing import Callable, Dict, List, Tuple

# --- Definición de la Paleta de Colores (Pilar 4) ---
PALETTE = {
    "primary": "#F2AED4",    # Rosa
    "secondary": "#F2E205",  # Amarillo
    "bg_dark": "#0D0D0D",    # Negro
    "bg_light": "#222222",   # Gris oscuro (para marcos)
    "text": "#FFFFFF",       # Blanco
    "success": "#00FF00",    # Verde
    "error": "#FF0000"       # Rojo
}

class App(customtkinter.CTk):
    """
    Clase principal de la interfaz gráfica (GUI) de la aplicación.
    
    Atributos:
        merge_use_case (Callable): Función del caso de uso para fusionar PDFs.
        input_dir (Path): Directorio de entrada de PDFs.
        output_dir (Path): Directorio de salida para el PDF fusionado.
        logo_file (Path): Ruta al archivo de logo.
    """
    
    def __init__(
        self, 
        merge_use_case: Callable,
        input_dir: Path,
        output_dir: Path,
        logo_file: Path,
        *args, 
        **kwargs
    ):
        """Inicializa la ventana principal de la aplicación."""
        super().__init__(*args, **kwargs)

        # 1. Inyección de Dependencias y Configuración de Rutas
        self.merge_use_case = merge_use_case
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = output_dir / "etiquetas_imprimir.pdf"
        self.logo_file = logo_file
        
        # Almacenamiento de checkboxes [ (ruta_pdf, widget_checkbox) ]
        self.checkboxes: Dict[str, List[Tuple[Path, customtkinter.CTkCheckBox]]] = {}

        # 2. Configuración de la Ventana y Tema
        customtkinter.set_appearance_mode("Dark")
        self.title("Fusionador de Etiquetas (Animall)")
        self.geometry("800x700")
        self.configure(fg_color=PALETTE["bg_dark"])

        # 3. Creación de Widgets
        self._setup_ui()
        
        # 4. Escaneo inicial de archivos
        self._scan_and_display_files()

    def _setup_ui(self):
        """Construye la interfaz de usuario estática."""
        
        # --- Cabecera con Logo ---
        try:
            pil_image = Image.open(self.logo_file)
            logo_image = customtkinter.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(300, 70) # Tamaño ajustado
            )
            logo_label = customtkinter.CTkLabel(
                self, text="", image=logo_image, fg_color="transparent"
            )
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            logo_label = customtkinter.CTkLabel(
                self, text="Animall Forrajería", 
                font=("Arial", 24, "bold"),
                text_color=PALETTE["primary"]
            )
            logo_label.pack(pady=20)

        # --- Marco principal con Scroll ---
        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=PALETTE["bg_light"]
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # --- Pie de Página (Botón y Estado) ---
        footer_frame = customtkinter.CTkFrame(
            self, fg_color=PALETTE["bg_dark"]
        )
        footer_frame.pack(fill="x", padx=30, pady=(10, 20))

        self.status_label = customtkinter.CTkLabel(
            footer_frame, 
            text="Listo. Selecciona los PDFs y presiona 'Generar'.",
            text_color=PALETTE["text"],
            height=30
        )
        self.status_label.pack(fill="x")

        self.generate_button = customtkinter.CTkButton(
            footer_frame,
            text="Generar PDF",
            command=self._on_generate,
            fg_color=PALETTE["primary"],
            text_color=PALETTE["bg_dark"],
            hover_color="#E09AC0", # Rosa más claro
            font=("", 16, "bold"),
            height=40
        )
        self.generate_button.pack(fill="x", pady=(10, 0))

    def _scan_and_display_files(self):
        """Escanea el directorio de entrada y muestra las categorías y archivos."""
        
        has_files = False
        for category_dir in sorted(self.input_dir.glob('*')):
            if not category_dir.is_dir():
                continue

            category_name = category_dir.name
            pdf_files = sorted(list(category_dir.glob('*.pdf')))
            
            if not pdf_files:
                continue # No mostrar categorías vacías

            has_files = True
            self.checkboxes[category_name] = []

            # Título de Categoría (Color Secundario)
            cat_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=category_name,
                font=("", 18, "bold"),
                text_color=PALETTE["secondary"]
            )
            cat_label.pack(anchor="w", pady=(15, 5), padx=10)

            # Checkboxes para cada PDF
            for pdf_file in pdf_files:
                chk = customtkinter.CTkCheckBox(
                    self.scroll_frame,
                    text=pdf_file.name,
                    text_color=PALETTE["text"],
                    fg_color=PALETTE["primary"], # Color del check
                    hover_color="#E09AC0"
                )
                chk.pack(anchor="w", padx=30, pady=2)
                self.checkboxes[category_name].append((pdf_file, chk))
        
        if not has_files:
            self.status_label.configure(
                text=f"No se encontraron PDFs. Agrega carpetas y PDFs en '{self.input_dir.name}'",
                text_color=PALETTE["secondary"]
            )

    def _on_generate(self):
        """Callback del botón 'Generar PDF'."""
        
        # 1. Feedback de Carga (UX - Pilar 4)
        self.status_label.configure(
            text="Procesando... por favor espera.", text_color=PALETTE["secondary"]
        )
        self.generate_button.configure(state="disabled")
        self.update_idletasks() # Forzar actualización de la GUI

        # 2. Recopilar archivos seleccionados
        selected_files: List[str] = []
        for category in self.checkboxes:
            for file_path, chk in self.checkboxes[category]:
                if chk.get() == 1: # 1 significa "marcado"
                    selected_files.append(str(file_path))

        # 3. Validación y Manejo de Errores
        if not selected_files:
            self.status_label.configure(
                text="Error: No se seleccionó ningún archivo.",
                text_color=PALETTE["error"]
            )
            self.generate_button.configure(state="normal")
            return

        # 4. Llamada al Caso de Uso (Core)
        try:
            self.merge_use_case(selected_files, str(self.output_file))
            
            # 5. Feedback de Éxito
            self.status_label.configure(
                text=f"¡Éxito! PDF guardado en '{self.output_dir.name}/{self.output_file.name}'",
                text_color=PALETTE["success"]
            )
            
            # (Opcional) Abrir la carpeta de salida
            # os.startfile(self.output_dir) 

        except Exception as e:
            # 5. Feedback de Error
            print(f"Error en el núcleo: {e}")
            self.status_label.configure(
                text=f"Error al generar el PDF: {e}",
                text_color=PALETTE["error"]
            )
        finally:
            # 6. Restaurar la GUI
            self.generate_button.configure(state="normal")