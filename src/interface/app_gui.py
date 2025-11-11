# src/interface/app_gui.py
import customtkinter
import os
import sys
import subprocess
import tkinter.messagebox  # Para el diálogo de "Sí/No"
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

# --- CONSTANTE PARA EL DISEÑO ---
CHECKBOX_COLUMNS = 3


class App(customtkinter.CTk):
    """
    Clase principal de la interfaz gráfica (GUI) de la aplicación.
    ... (el resto del docstring es igual) ...
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
        # ... (Esta función no cambia en absoluto) ...
        
        # --- Cabecera con Logo ---
        try:
            pil_image = Image.open(self.logo_file)
            logo_image = customtkinter.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(300, 70) 
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
        self.scroll_frame.grid_columnconfigure(0, weight=1)

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
        """
        Escanea el directorio de entrada y muestra las categorías y archivos.
        """
        # ... (Esta función no cambia en absoluto) ...
        
        has_files = False
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for category_dir in sorted(self.input_dir.glob('*')):
            if not category_dir.is_dir():
                continue

            category_name = category_dir.name
            pdf_files = sorted(list(category_dir.glob('*.pdf')))
            
            if not pdf_files:
                continue

            has_files = True
            self.checkboxes[category_name] = []

            # --- Título de Categoría ---
            cat_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=category_name,
                font=("", 18, "bold"),
                text_color=PALETTE["secondary"]
            )
            cat_label.pack(anchor="w", pady=(15, 5), padx=10)

            # --- Marco de Cuadrícula (Grid) para los Checkboxes ---
            grid_frame = customtkinter.CTkFrame(
                self.scroll_frame, fg_color="transparent"
            )
            grid_frame.pack(fill="x", anchor="w", padx=20) 

            grid_frame.columnconfigure(
                tuple(range(CHECKBOX_COLUMNS)), weight=1
            )

            # --- Checkboxes en Cuadrícula (Grid) ---
            for index, pdf_file in enumerate(pdf_files):
                row = index // CHECKBOX_COLUMNS
                col = index % CHECKBOX_COLUMNS
                
                chk = customtkinter.CTkCheckBox(
                    grid_frame, 
                    text=pdf_file.name,
                    text_color=PALETTE["text"],
                    fg_color=PALETTE["primary"], 
                    hover_color="#E09AC0"
                )
                chk.grid(row=row, column=col, sticky="w", padx=10, pady=2)
                
                self.checkboxes[category_name].append((pdf_file, chk))
        
        if not has_files:
            self.status_label.configure(
                text=f"No se encontraron PDFs. Agrega carpetas y PDFs en '{self.input_dir.name}'",
                text_color=PALETTE["secondary"]
            )
            
    # --- NUEVA FUNCIÓN AUXILIAR ---
    def _open_output_folder(self):
        """
        Abre la carpeta de salida (_SALIDA) en el explorador de 
        archivos del sistema operativo.
        """
        try:
            if sys.platform == "win32":
                os.startfile(self.output_dir)
            elif sys.platform == "darwin": # macOS
                subprocess.run(["open", self.output_dir])
            else: # Linux
                subprocess.run(["xdg-open", self.output_dir])
        except Exception as e:
            print(f"Error al abrir la carpeta: {e}")
            self.status_label.configure(
                text=f"Error al abrir la carpeta: {e}",
                text_color=PALETTE["error"]
            )

    # --- FUNCIÓN MODIFICADA ---
    def _on_generate(self):
        """
        Callback del botón 'Generar PDF'.
        *** ESTA ES LA FUNCIÓN ACTUALIZADA ***
        """
        
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
            success_msg = f"¡Éxito! PDF guardado en '{self.output_dir.name}/{self.output_file.name}'"
            self.status_label.configure(
                text=success_msg,
                text_color=PALETTE["success"]
            )

            # --- ¡NUEVA CARACTERÍSTICA! ---
            # Levantar la ventana principal por si estaba minimizada
            self.attributes("-topmost", True)
            self.update_idletasks()
            self.attributes("-topmost", False)

            # Usamos messagebox de tkinter. Es simple y efectivo.
            open_folder = tkinter.messagebox.askyesno(
                "Fusión Completada",
                "¡Éxito! El PDF se ha generado.\n\n"
                f"¿Deseas abrir la carpeta de salida ahora?",
                icon='question'
            )
            
            if open_folder:
                self._open_output_folder()
            # --- FIN DE LA NUEVA CARACTERÍSTICA ---

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