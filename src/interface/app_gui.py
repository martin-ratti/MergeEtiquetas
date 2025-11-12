# src/interface/app_gui.py
import customtkinter
import os
import sys
import subprocess
import tkinter.messagebox
from PIL import Image
from pathlib import Path
from typing import Callable, Dict, List, Tuple

# Paleta de colores de la marca (Pilar 4)
PALETTE = {
    "primary": "#F2AED4",    # Rosa
    "secondary": "#F2E205",  # Amarillo
    "bg_dark": "#0D0D0D",    # Negro
    "bg_light": "#222222",   # Gris oscuro (para marcos)
    "bg_hover": "#2A2A2A",   # Gris más claro para hover
    "text": "#FFFFFF",       # Blanco
    "success": "#00FF00",    # Verde
    "error": "#FF0000"       # Rojo
}

# Constante de diseño de la cuadrícula
CHECKBOX_COLUMNS = 3


class CategoryCard(customtkinter.CTkFrame):
    """
    Una Tarjeta de widget personalizada que encapsula una categoría.
    
    Gestiona sus propios eventos de <Enter> y <Leave> para cambiar
    su color de fondo, proporcionando feedback visual interactivo.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, 
                         fg_color=PALETTE["bg_light"], 
                         corner_radius=10, 
                         *args, **kwargs)
        
        self.base_color = PALETTE["bg_light"]
        self.hover_color = PALETTE["bg_hover"]
        
        # Vincular eventos de ratón al frame principal
        self.bind("<Enter>", self._on_mouse_enter)
        self.bind("<Leave>", self._on_mouse_leave)
        
        # Vincular eventos a todos los widgets hijos recursivamente
        self.bind_children_events(self)

    def bind_children_events(self, widget):
        """
        Vincula recursivamente los eventos <Enter> y <Leave> a todos los hijos.
        
        Esto es crucial para que el hover no se "cancele" al pasar
        el ratón sobre un widget hijo (como un checkbox o un label).
        """
        for child in widget.winfo_children():
            if not isinstance(child, customtkinter.CTkScrollbar):
                child.bind("<Enter>", self._on_mouse_enter, add='+')
                child.bind("<Leave>", self._on_mouse_leave, add='+')
                self.bind_children_events(child)

    def _on_mouse_enter(self, event):
        """Callback para cuando el ratón entra en la tarjeta."""
        self.configure(fg_color=self.hover_color)

    def _on_mouse_leave(self, event):
        """Callback para cuando el ratón sale de la tarjeta."""
        self.configure(fg_color=self.base_color)


class App(customtkinter.CTk):
    """
    Clase principal de la interfaz gráfica (GUI) de la aplicación.
    
    Orquesta la UI, gestiona el estado de los widgets y llama
    al caso de uso (inyectado) cuando el usuario lo solicita.
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
        """
        Inicializa la ventana principal de la aplicación.

        Args:
            merge_use_case (Callable): La función del caso de uso a ejecutar.
            input_dir (Path): Ruta a la carpeta de PDFs de entrada.
            output_dir (Path): Ruta a la carpeta de salida.
            logo_file (Path): Ruta al archivo de logo.
        """
        super().__init__(*args, **kwargs)

        # Inyección de Dependencias
        self.merge_use_case = merge_use_case
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = output_dir / "etiquetas_imprimir.pdf"
        self.logo_file = logo_file
        
        # Almacenamiento del estado de los widgets
        self.child_checkboxes: Dict[str, List[Tuple[Path, customtkinter.CTkCheckBox]]] = {}
        self.master_checkboxes: Dict[str, customtkinter.CTkCheckBox] = {}

        # Definición de la jerarquía de fuentes
        self.font_titulo_categoria = customtkinter.CTkFont(size=22, weight="bold")
        self.font_checkbox_master = customtkinter.CTkFont(size=15, weight="normal")
        self.font_checkbox_hijo = customtkinter.CTkFont(size=12)

        # Configuración de la Ventana
        customtkinter.set_appearance_mode("Dark")
        self.title("Fusionador de Etiquetas (Animall)")
        self.geometry("800x700") 
        self.configure(fg_color=PALETTE["bg_dark"])

        # Construir y poblar la UI
        self._setup_ui()
        self._scan_and_display_files()
        self._update_generate_button_state()

    def _setup_ui(self):
        """Construye la interfaz de usuario estática (widgets principales)."""
        
        try:
            pil_image = Image.open(self.logo_file)
            logo_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(300, 70))
            logo_label = customtkinter.CTkLabel(self, text="", image=logo_image, fg_color="transparent")
            logo_label.pack(pady=20)
        except Exception as e:
            # Fallback en caso de que falte el logo
            print(f"Error al cargar el logo: {e}")
            logo_label = customtkinter.CTkLabel(self, text="Animall Forrajería", font=("Arial", 24, "bold"), text_color=PALETTE["primary"])
            logo_label.pack(pady=20)

        # El frame principal usa el color de fondo para que las tarjetas resalten
        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self, 
            fg_color=PALETTE["bg_dark"],
            corner_radius=0
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Contenedor para el pie de página
        footer_frame = customtkinter.CTkFrame(self, fg_color=PALETTE["bg_dark"])
        footer_frame.pack(fill="x", padx=30, pady=(10, 20))

        self.status_label = customtkinter.CTkLabel(footer_frame, text="Listo.", text_color=PALETTE["text"], height=30)
        self.status_label.pack(fill="x")

        self.generate_button = customtkinter.CTkButton(
            footer_frame,
            text="Generar PDF", # El texto se actualiza dinámicamente
            command=self._on_generate,
            fg_color=PALETTE["primary"],
            text_color=PALETTE["bg_dark"],
            hover_color="#E09AC0",
            font=("", 16, "bold"),
            height=40,
            corner_radius=10
        )
        self.generate_button.pack(fill="x", pady=(10, 0))


    def _scan_and_display_files(self):
        """
        Escanea el directorio de entrada y puebla la UI
        creando 'Tarjetas de Categoría' interactivas.
        """
        
        has_files = False
        
        # Limpiar widgets antiguos antes de volver a escanear
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        # Itera sobre las subcarpetas (categorías)
        for category_dir in sorted(self.input_dir.glob('*')):
            if not category_dir.is_dir():
                continue

            category_name = category_dir.name
            pdf_files = sorted(list(category_dir.glob('*.pdf')))
            
            if not pdf_files:
                continue # No mostrar categorías vacías

            has_files = True
            self.child_checkboxes[category_name] = []
            
            # 1. Crear la Tarjeta contenedora
            card = CategoryCard(master=self.scroll_frame)
            card.pack(fill="x", pady=(0, 10))

            # 2. Crear la cabecera (Título + Checkbox Maestro)
            header_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", anchor="w", pady=(15, 5), padx=20)

            cat_label = customtkinter.CTkLabel(
                header_frame,
                text=category_name,
                font=self.font_titulo_categoria,
                text_color=PALETTE["secondary"]
            )
            cat_label.pack(side="left", anchor="w")

            master_chk = customtkinter.CTkCheckBox(
                header_frame,
                text=f"Seleccionar Todos ({len(pdf_files)})",
                text_color=PALETTE["text"],
                fg_color=PALETTE["primary"],
                hover_color="#E09AC0",
                font=self.font_checkbox_master
            )
            master_chk.pack(side="left", anchor="w", padx=20)
            
            self.master_checkboxes[category_name] = master_chk

            # 3. Crear la cuadrícula de checkboxes hijos
            grid_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            grid_frame.pack(fill="x", anchor="w", padx=30, pady=(0, 15)) 
            grid_frame.columnconfigure(
                tuple(range(CHECKBOX_COLUMNS)), weight=1
            )
            
            child_widgets_in_category = []

            for index, pdf_file in enumerate(pdf_files):
                row = index // CHECKBOX_COLUMNS
                col = index % CHECKBOX_COLUMNS
                
                child_chk = customtkinter.CTkCheckBox(
                    grid_frame,
                    text=pdf_file.name,
                    text_color=PALETTE["text"],
                    fg_color=PALETTE["primary"], 
                    hover_color="#E09AC0",
                    font=self.font_checkbox_hijo
                )
                child_chk.grid(row=row, column=col, sticky="w", padx=10, pady=4)
                
                self.child_checkboxes[category_name].append((pdf_file, child_chk))
                child_widgets_in_category.append(child_chk)
                
                # Asignar comando al hijo para actualizar el estado general
                child_chk.configure(
                    command=self._update_generate_button_state
                )
            
            # Asignar comando al maestro para controlar a sus hijos
            master_chk.configure(
                command=lambda master=master_chk, 
                children=child_widgets_in_category: \
                    self._on_master_toggle(master, children)
            )
            
            # Propagar eventos de hover de la tarjeta a sus hijos
            card.bind_children_events(card)
        
        if not has_files:
            self.status_label.configure(
                text=f"No se encontraron PDFs. Agrega carpetas y PDFs en '{self.input_dir.name}'",
                text_color=PALETTE["secondary"]
            )
            

    def _on_master_toggle(self, master_checkbox, child_checkboxes):
        """Callback: El checkbox maestro controla a sus hijos."""
        is_selected = master_checkbox.get()
        
        for child in child_checkboxes:
            if is_selected:
                child.select()
            else:
                child.deselect()
        
        self._update_generate_button_state()

    def _update_generate_button_state(self):
        """
        Actualiza el estado y texto del botón "Generar PDF".
        
        Esta es la "única fuente de verdad" para el estado del botón.
        También sincroniza el estado de los checkboxes maestros.
        """
        total_selected = 0
        
        for category_name, child_list in self.child_checkboxes.items():
            count_in_category = 0
            for _, child_chk in child_list:
                if child_chk.get() == 1:
                    total_selected += 1
                    count_in_category += 1

            # Sincronizar el checkbox maestro basado en sus hijos
            master_chk = self.master_checkboxes.get(category_name)
            if master_chk:
                if count_in_category == 0:
                    master_chk.deselect()
                elif count_in_category == len(child_list):
                    master_chk.select()
                else:
                     master_chk.deselect() # Estado mixto se muestra como deseleccionado

        # Actualizar el botón de generar
        if total_selected == 0:
            self.generate_button.configure(
                text="Selecciona etiquetas para generar",
                state="disabled"
            )
            self.status_label.configure(text="Listo.")
        else:
            plural = "etiqueta" if total_selected == 1 else "etiquetas"
            self.generate_button.configure(
                text=f"Generar PDF ({total_selected} {plural})",
                state="normal"
            )
            self.status_label.configure(text=f"{total_selected} {plural} seleccionada(s).")
            
    def _clear_all_checkboxes(self):
        """Deselecciona todas las casillas (maestras e hijas) en la app."""
        for master_chk in self.master_checkboxes.values():
            master_chk.deselect()
            
        for child_list in self.child_checkboxes.values():
            for _, child_chk in child_list:
                child_chk.deselect()
        
        # Sincronizar el botón para que vuelva a "deshabilitado"
        self._update_generate_button_state()

    def _open_output_folder(self):
        """Abre la carpeta de salida en el explorador de archivos (multiplataforma)."""
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

    def _on_generate(self):
        """Callback del botón "Generar PDF"."""
        
        # 1. Dar feedback de "Cargando"
        self.status_label.configure(
            text="Procesando... por favor espera.", text_color=PALETTE["secondary"]
        )
        self.generate_button.configure(state="disabled")
        self.update_idletasks() # Forzar actualización de la GUI

        # 2. Recopilar archivos seleccionados
        selected_files: List[str] = []
        for category in self.child_checkboxes:
            for file_path, chk in self.child_checkboxes[category]:
                if chk.get() == 1:
                    selected_files.append(str(file_path))

        # 3. Llamar al núcleo (try/except)
        try:
            self.merge_use_case(selected_files, str(self.output_file))
            
            # 4. Feedback de Éxito
            success_msg = f"¡Éxito! PDF guardado en '{self.output_dir.name}/{self.output_file.name}'"
            self.status_label.configure(
                text=success_msg,
                text_color=PALETTE["success"]
            )
            
            # 5. Limpieza automática
            self._clear_all_checkboxes()
            
            # Traer la ventana al frente para mostrar el diálogo
            self.attributes("-topmost", True)
            self.update_idletasks()
            self.attributes("-topmost", False)

            # 6. Preguntar al usuario si desea abrir la carpeta
            open_folder = tkinter.messagebox.askyesno(
                "Fusión Completada",
                "¡Éxito! El PDF se ha generado.\n\n"
                f"¿Deseas abrir la carpeta de salida ahora?",
                icon='question'
            )
            
            if open_folder:
                self._open_output_folder()

        except Exception as e:
            # 7. Feedback de Error
            print(f"Error en el núcleo: {e}")
            self.status_label.configure(
                text=f"Error al generar el PDF: {e}",
                text_color=PALETTE["error"]
            )
            # Restaurar el botón en caso de error
            self._update_generate_button_state()