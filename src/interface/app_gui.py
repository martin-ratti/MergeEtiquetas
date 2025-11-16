# src/interface/app_gui.py
import customtkinter
import os
import sys
import subprocess
import tkinter.messagebox
import configparser
from PIL import Image
from pathlib import Path
from typing import Callable, Dict, List, Tuple

# Paleta de colores
PALETTE = {
    "primary": "#F2AED4",
    "secondary": "#F2E205",
    "bg_dark": "#0D0D0D",
    "bg_light": "#222222",
    "bg_hover": "#2A2A2A",
    "text": "#FFFFFF",
    "success": "#00FF00",
    "error": "#FF0000"
}
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
        
        self.bind("<Enter>", self._on_mouse_enter)
        self.bind("<Leave>", self._on_mouse_leave)
        self.bind_children_events(self)

    def bind_children_events(self, widget):
        """Vincula recursivamente los eventos <Enter> y <Leave> a todos los hijos."""
        for child in widget.winfo_children():
            if not isinstance(child, customtkinter.CTkScrollbar):
                child.bind("<Enter>", self._on_mouse_enter, add='+')
                child.bind("<Leave>", self._on_mouse_leave, add='+')
                self.bind_children_events(child)

    def _on_mouse_enter(self, event):
        self.configure(fg_color=self.hover_color)

    def _on_mouse_leave(self, event):
        self.configure(fg_color=self.base_color)


class App(customtkinter.CTk):
    """
    Clase principal de la interfaz gráfica (GUI) de la aplicación.
    """
    
    def __init__(
        self, 
        merge_use_case: Callable,
        send_email_use_case: Callable, 
        input_dir: Path,
        output_dir: Path,
        logo_file: Path,
        config_file: Path,
        *args, 
        **kwargs
    ):
        """Inicializa la ventana principal de la aplicación."""
        super().__init__(*args, **kwargs)

        # Inyección de Dependencias
        self.merge_use_case = merge_use_case
        self.send_email_use_case = send_email_use_case
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_file = output_dir / "etiquetas_imprimir.pdf"
        self.logo_file = logo_file
        self.config_file = config_file
        
        # Almacenamiento del estado de la UI
        self.child_checkboxes: Dict[str, List[Tuple[Path, customtkinter.CTkCheckBox]]] = {}
        self.master_checkboxes: Dict[str, customtkinter.CTkCheckBox] = {}
        self.font_titulo_categoria = customtkinter.CTkFont(size=22, weight="bold")
        self.font_checkbox_master = customtkinter.CTkFont(size=15, weight="normal")
        self.font_checkbox_hijo = customtkinter.CTkFont(size=12)
        
        # --- MODIFICADO: Eliminamos el flag 'pdf_generated_successfully' ---
        self.email_config: Dict[str, str] | None = None

        # Configuración de la Ventana
        customtkinter.set_appearance_mode("Dark")
        self.title("Fusionador de Etiquetas (Animall)")
        self.geometry("800x750")
        self.configure(fg_color=PALETTE["bg_dark"])

        # Construir y poblar la UI
        self._setup_ui()
        self._load_email_config()
        self._scan_and_display_files()
        self._update_button_states()

    def _setup_ui(self):
        """Construye la interfaz de usuario estática (widgets principales)."""
        
        try:
            pil_image = Image.open(self.logo_file)
            logo_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(300, 70))
            logo_label = customtkinter.CTkLabel(self, text="", image=logo_image, fg_color="transparent")
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            logo_label = customtkinter.CTkLabel(self, text="Animall Forrajería", font=("Arial", 24, "bold"), text_color=PALETTE["primary"])
            logo_label.pack(pady=20)

        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=PALETTE["bg_dark"], corner_radius=0
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        footer_frame = customtkinter.CTkFrame(self, fg_color=PALETTE["bg_dark"])
        footer_frame.pack(fill="x", padx=30, pady=(10, 20))

        self.status_label = customtkinter.CTkLabel(footer_frame, text="Listo.", text_color=PALETTE["text"], height=30)
        self.status_label.pack(fill="x")

        self.generate_button = customtkinter.CTkButton(
            footer_frame,
            text="Generar PDF",
            command=self._on_generate,
            fg_color=PALETTE["primary"],
            text_color=PALETTE["bg_dark"],
            hover_color="#E09AC0",
            font=("", 16, "bold"),
            height=40,
            corner_radius=10
        )
        self.generate_button.pack(fill="x", pady=(5, 5))

        self.email_button = customtkinter.CTkButton(
            footer_frame,
            text="Enviar PDF por Email",
            command=self._on_send_email,
            fg_color=PALETTE["secondary"],
            text_color=PALETTE["bg_dark"],
            hover_color="#D0C204",
            font=("", 16, "bold"),
            height=40,
            corner_radius=10
        )
        self.email_button.pack(fill="x", pady=(5, 0))

    
    def _load_email_config(self):
        """Intenta leer el config.ini y almacena la configuración."""
        try:
            parser = configparser.ConfigParser()
            if not self.config_file.exists():
                raise FileNotFoundError(f"'{self.config_file.name}' no encontrado.")
                
            parser.read(self.config_file)
            
            config = dict(parser['Email'])
            required_keys = ['email_emisor', 'app_password', 'email_receptor', 'asunto']
            if not all(key in config for key in required_keys):
                raise configparser.NoOptionError("Alguna clave", "Email")
                
            self.email_config = {key.upper(): val for key, val in config.items()}
            print("Configuración de email cargada exitosamente.")
            
        except FileNotFoundError:
            self.status_label.configure(
                text="Aviso: 'config.ini' no encontrado. El envío de email está deshabilitado.",
                text_color=PALETTE["secondary"]
            )
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.status_label.configure(
                text="Error: 'config.ini' está incompleto. El envío de email está deshabilitado.",
                text_color=PALETTE["error"]
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Error al leer 'config.ini': {e}",
                text_color=PALETTE["error"]
            )


    def _scan_and_display_files(self):
        """Escanea el directorio y puebla la UI con Tarjetas de Categoría."""
        has_files = False
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for category_dir in sorted(self.input_dir.glob('*')):
            if not category_dir.is_dir(): continue
            category_name = category_dir.name
            pdf_files = sorted(list(category_dir.glob('*.pdf')))
            if not pdf_files: continue

            has_files = True
            self.child_checkboxes[category_name] = []
            
            card = CategoryCard(master=self.scroll_frame)
            card.pack(fill="x", pady=(0, 10))
            header_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", anchor="w", pady=(15, 5), padx=20)
            cat_label = customtkinter.CTkLabel(header_frame, text=category_name, font=self.font_titulo_categoria, text_color=PALETTE["secondary"])
            cat_label.pack(side="left", anchor="w")

            master_chk = customtkinter.CTkCheckBox(
                header_frame, text=f"Seleccionar Todos ({len(pdf_files)})",
                text_color=PALETTE["text"], fg_color=PALETTE["primary"],
                hover_color="#E09AC0", font=self.font_checkbox_master
            )
            master_chk.pack(side="left", anchor="w", padx=20)
            self.master_checkboxes[category_name] = master_chk

            grid_frame = customtkinter.CTkFrame(card, fg_color="transparent")
            grid_frame.pack(fill="x", anchor="w", padx=30, pady=(0, 15)) 
            grid_frame.columnconfigure(tuple(range(CHECKBOX_COLUMNS)), weight=1)
            
            child_widgets_in_category = []
            for index, pdf_file in enumerate(pdf_files):
                row = index // CHECKBOX_COLUMNS
                col = index % CHECKBOX_COLUMNS
                child_chk = customtkinter.CTkCheckBox(
                    grid_frame, text=pdf_file.name, text_color=PALETTE["text"],
                    fg_color=PALETTE["primary"], hover_color="#E09AC0",
                    font=self.font_checkbox_hijo
                )
                child_chk.grid(row=row, column=col, sticky="w", padx=10, pady=4)
                self.child_checkboxes[category_name].append((pdf_file, child_chk))
                child_widgets_in_category.append(child_chk)
                child_chk.configure(command=self._update_button_states)
            
            master_chk.configure(
                command=lambda m=master_chk, c=child_widgets_in_category: \
                    self._on_master_toggle(m, c)
            )
            card.bind_children_events(card)
        
        if not has_files and not self.email_config:
            self.status_label.configure(
                text=f"No se encontraron PDFs. Agrega carpetas y PDFs en '{self.input_dir.name}'",
                text_color=PALETTE["secondary"]
            )
            
    def _on_master_toggle(self, master_checkbox, child_checkboxes):
        is_selected = master_checkbox.get()
        for child in child_checkboxes:
            if is_selected: child.select()
            else: child.deselect()
        self._update_button_states()

    # --- ¡FUNCIÓN MODIFICADA! ---
    def _update_button_states(self):
        """
        Actualiza el estado de TODOS los botones (Generar y Email)
        basado en el estado actual de la UI y del sistema de archivos.
        """
        total_selected = 0
        for category_name, child_list in self.child_checkboxes.items():
            count_in_category = 0
            for _, child_chk in child_list:
                if child_chk.get() == 1:
                    total_selected += 1
                    count_in_category += 1
            master_chk = self.master_checkboxes.get(category_name)
            if master_chk:
                if count_in_category == 0: master_chk.deselect()
                elif count_in_category == len(child_list): master_chk.select()
                else: master_chk.deselect() 

        # --- Lógica del Botón Generar PDF ---
        if total_selected == 0:
            self.generate_button.configure(
                text="Selecciona etiquetas para generar", state="disabled"
            )
            if not self.email_config and not self.status_label.cget("text").startswith("Aviso"):
                self.status_label.configure(text="Listo.")
        else:
            plural = "etiqueta" if total_selected == 1 else "etiquetas"
            self.generate_button.configure(
                text=f"Generar PDF ({total_selected} {plural})", state="normal"
            )
            self.status_label.configure(text=f"{total_selected} {plural} seleccionada(s).")

        # --- ¡NUEVA LÓGICA DE BOTÓN DE EMAIL! ---
        # El estado solo depende de dos cosas:
        # 1. ¿Está cargada la configuración del email?
        # 2. ¿Existe físicamente el archivo PDF a enviar?
        pdf_exists = self.output_file.exists()
        
        if self.email_config and pdf_exists:
            self.email_button.configure(state="normal")
        else:
            self.email_button.configure(state="disabled")
            
    # --- ¡FUNCIÓN MODIFICADA! ---
    def _clear_all_checkboxes(self):
        """Deselecciona todas las casillas (maestras e hijas) en la app."""
        for master_chk in self.master_checkboxes.values():
            master_chk.deselect()
        for child_list in self.child_checkboxes.values():
            for _, child_chk in child_list:
                child_chk.deselect()
        
        # Ya no gestionamos el flag. Solo actualizamos los botones.
        self._update_button_states()

    def _open_output_folder(self):
        """Abre la carpeta de salida en el explorador de archivos (multiplataforma)."""
        try:
            if sys.platform == "win32": os.startfile(self.output_dir)
            elif sys.platform == "darwin": subprocess.run(["open", self.output_dir])
            else: subprocess.run(["xdg-open", self.output_dir])
        except Exception as e:
            print(f"Error al abrir la carpeta: {e}")
            self.status_label.configure(text=f"Error: {e}", text_color=PALETTE["error"])

    # --- ¡FUNCIÓN MODIFICADA! ---
    def _on_generate(self):
        """Callback del botón "Generar PDF"."""
        self.status_label.configure(text="Procesando...", text_color=PALETTE["secondary"])
        self.generate_button.configure(state="disabled")
        self.email_button.configure(state="disabled") # Deshabilitar mientras se genera
        self.update_idletasks()

        selected_files: List[str] = []
        for category in self.child_checkboxes:
            for file_path, chk in self.child_checkboxes[category]:
                if chk.get() == 1: selected_files.append(str(file_path))

        try:
            self.merge_use_case(selected_files, str(self.output_file))
            
            success_msg = f"¡Éxito! PDF guardado en '{self.output_dir.name}'"
            self.status_label.configure(text=success_msg, text_color=PALETTE["success"])
            
            # --- MODIFICADO ---
            # Ya no establecemos 'self.pdf_generated_successfully = True'
            
            self._clear_all_checkboxes() # Esto llama a _update_button_states
            
            self.attributes("-topmost", True); self.update_idletasks(); self.attributes("-topmost", False)

            open_folder = tkinter.messagebox.askyesno(
                "Fusión Completada",
                "¡Éxito! El PDF se ha generado.\n\n"
                f"¿Deseas abrir la carpeta de salida ahora?",
                icon='question'
            )
            if open_folder: self._open_output_folder()

        except Exception as e:
            print(f"Error en el núcleo: {e}")
            self.status_label.configure(text=f"Error al generar PDF: {e}", text_color=PALETTE["error"])
            # --- MODIFICADO ---
            # Ya no establecemos 'self.pdf_generated_successfully = False'
            self._update_button_states() # Restaurar estado de botones
            
    # --- ¡FUNCIÓN MODIFICADA! ---
    def _on_send_email(self):
        """Callback del botón "Enviar PDF por Email"."""
        self.status_label.configure(text="Enviando email...", text_color=PALETTE["secondary"])
        self.email_button.configure(state="disabled") # Deshabilitar mientras se envía
        self.generate_button.configure(state="disabled") # Deshabilitar para evitar conflictos
        self.update_idletasks()
        
        try:
            self.send_email_use_case(
                config=self.email_config,
                pdf_path=str(self.output_file)
            )
            
            self.status_label.configure(
                text=f"Email enviado a {self.email_config['EMAIL_RECEPTOR']}",
                text_color=PALETTE["success"]
            )
            # El botón se mantiene activo (porque el PDF y el config siguen siendo válidos)
            self._update_button_states() 

        except (ValueError, RuntimeError) as e:
            print(f"Error en el núcleo de email: {e}")
            self.status_label.configure(text=f"Error: {e}", text_color=PALETTE["error"])
            # Restaurar botones al estado pre-envío
            self._update_button_states()