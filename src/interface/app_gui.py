# src/interface/app_gui.py
import customtkinter
import os
import sys
import threading
import subprocess
import tkinter.messagebox
import tkinter.ttk as ttk
import configparser
from PIL import Image
from pathlib import Path
from src.core.exceptions import MergeError, EmailError
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
    Se ha simplificado para mejorar el rendimiento del scroll.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, 
                         fg_color=PALETTE["bg_light"], 
                         corner_radius=10, 
                         *args, **kwargs)


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

        # Barra de herramientas superior (Refresh)
        toolbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        self.refresh_btn = customtkinter.CTkButton(
            toolbar_frame, 
            text="Refrescar Lista", 
            command=self._scan_and_display_files,
            width=100,
            height=30,
            fg_color=PALETTE["bg_light"],
            hover_color=PALETTE["bg_hover"]
        )
        self.refresh_btn.pack(side="right")

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

        self.progress_bar = customtkinter.CTkProgressBar(footer_frame, height=15)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar.pack_forget() # Ocultar inicialmente

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
            # card.bind_children_events(card) # Removed for performance
        
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

        # Lógica del Botón Generar PDF
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

        # Lógica del Botón Enviar Email
        pdf_exists = self.output_file.exists()
        
        if self.email_config and pdf_exists:
            self.email_button.configure(state="normal")
        else:
            self.email_button.configure(state="disabled")
            
    def _clear_all_checkboxes(self):
        """Deselecciona todas las casillas (maestras e hijas) en la app."""
        for master_chk in self.master_checkboxes.values():
            master_chk.deselect()
        for child_list in self.child_checkboxes.values():
            for _, child_chk in child_list:
                child_chk.deselect()
        
        self._update_button_states()

    def _open_output_folder(self):
        """Abre la carpeta de salida en el explorador de archivos (multiplataforma)."""
        # Esta función ahora no se usa, pero la dejamos por si se reutiliza
        try:
            if sys.platform == "win32": os.startfile(self.output_dir)
            elif sys.platform == "darwin": subprocess.run(["open", self.output_dir])
            else: subprocess.run(["xdg-open", self.output_dir])
        except Exception as e:
            print(f"Error al abrir la carpeta: {e}")
            self.status_label.configure(text=f"Error: {e}", text_color=PALETTE["error"])

    def start_merge_thread(self):
        """Inicia el proceso de fusión en un hilo separado."""
        files = self.files_list
        if not files:
            messagebox.showwarning("Advertencia", "No hay archivos para unir.")
            return

        destination = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if not destination:
            return

        self.progress_bar.set(0)
        self.status_label.configure(text="Procesando...")
        self.merge_button.configure(state="disabled")

        def task():
            try:
                # Usamos el caso de uso inyectado
                self.merge_use_case(
                    files=files, 
                    output=destination, 
                    on_progress=self.update_progress
                )
                self.after(0, lambda: messagebox.showinfo("Éxito", "¡Fusión completada correctamente!"))
                self.after(0, lambda: self.status_label.configure(text="Listo"))
            except MergeError as e:
                 self.after(0, lambda: messagebox.showerror("Error de Fusión", str(e)))
                 self.after(0, lambda: self.status_label.configure(text="Error"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error Inesperado", f"Ocurrió un error grave: {e}"))
                self.after(0, lambda: self.status_label.configure(text="Error Grave"))
            finally:
                self.after(0, lambda: self.merge_button.configure(state="normal"))
                self.after(0, lambda: self.progress_bar.set(0))

        threading.Thread(target=task, daemon=True).start()

    def start_send_email_thread(self):
        """Inicia el proceso de envío de email en un hilo separado."""
        # Verificar config al inicio
        if not self.config_file.exists():
             messagebox.showwarning("Falta Configuración", f"No se encontró {self.config_file}")
             return
             
        # Leer config
        import configparser
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        email_config = {}
        try:
             email_config['EMAIL_EMISOR'] = config['DEFAULT'].get('EMAIL_EMISOR', '')
             email_config['APP_PASSWORD'] = config['DEFAULT'].get('APP_PASSWORD', '')
             if 'EMAIL_RECEPTOR' in config['DEFAULT']:
                email_config['EMAIL_RECEPTOR'] = config['DEFAULT']['EMAIL_RECEPTOR']
             else:
                 # Preguntar al usuario si no está en config
                 pass
             email_config['ASUNTO'] = config['DEFAULT'].get('ASUNTO', 'Etiquetas')
        except Exception as e:
             messagebox.showerror("Error Config", f"Error leyendo config.ini: {e}")
             return

        # Si falta receptor, pedirlo (simplificación)
        if 'EMAIL_RECEPTOR' not in email_config or not email_config['EMAIL_RECEPTOR']:
             dest = filedialog.askstring("Destinatario", "Ingrese email del destinatario:")
             if not dest: return
             email_config['EMAIL_RECEPTOR'] = dest
             
        # Pedir archivo a enviar (o usar el último generado si tuviéramos estado)
        # Por ahora pedimos seleccionar
        file_to_send = filedialog.askopenfilename(
             title="Seleccionar PDF para enviar",
             filetypes=[("Archivos PDF", "*.pdf")]
        )
        if not file_to_send:
             return

        self.send_email_button.configure(state="disabled")
        self.status_label.configure(text="Enviando email...")

        def task():
            try:
                 self.send_email_use_case(email_config, file_to_send)
                 self.after(0, lambda: messagebox.showinfo("Éxito", "Email enviado correctamente."))
                 self.after(0, lambda: self.status_label.configure(text="Email enviado"))
            except EmailError as e:
                  self.after(0, lambda: messagebox.showerror("Error de Email", str(e)))
                  self.after(0, lambda: self.status_label.configure(text="Error Envío"))
            except Exception as e:
                 self.after(0, lambda: messagebox.showerror("Error", f"Error inesperado: {e}"))
            finally:
                 self.after(0, lambda: self.send_email_button.configure(state="normal"))

        threading.Thread(target=task, daemon=True).start()

    def _update_progress_safe(self, current, total):
        """Callback seguro para hilos."""
        progress = current / total if total > 0 else 0
        self.after(0, lambda: self.progress_bar.set(progress))

    def _on_merge_success(self):
        success_msg = f"¡Éxito! PDF guardado en '{self.output_dir.name}'"
        self.status_label.configure(text=success_msg, text_color=PALETTE["success"])
        self.progress_bar.pack_forget()
        self._clear_all_checkboxes()
        self._set_ui_state("normal")

    def _on_merge_error(self, error):
        print(f"Error en el núcleo: {error}")
        self.status_label.configure(text=f"Error al generar PDF: {error}", text_color=PALETTE["error"])
        self.progress_bar.pack_forget()
        self._set_ui_state("normal")
        self._update_button_states()

    def _set_ui_state(self, state):
        """Habilita o deshabilita botones críticos."""
        self.generate_button.configure(state=state)
        self.email_button.configure(state=state if self.email_config and self.output_file.exists() else "disabled")
        self.refresh_btn.configure(state=state)

    def _on_send_email(self):
        """Callback del botón "Enviar PDF por Email" (Asíncrono)."""
        self.status_label.configure(text="Enviando email...", text_color=PALETTE["secondary"])
        self._set_ui_state("disabled")
        
        def run_email():
            try:
                self.send_email_use_case(
                    config=self.email_config,
                    pdf_path=str(self.output_file)
                )
                self.after(0, self._on_email_success)
            except Exception as e:
                self.after(0, lambda: self._on_email_error(e))
        
        threading.Thread(target=run_email, daemon=True).start()
    
    def _on_email_success(self):
        self.status_label.configure(
            text=f"Email enviado a {self.email_config['EMAIL_RECEPTOR']}",
            text_color=PALETTE["success"]
        )
        self._set_ui_state("normal")

    def _on_email_error(self, error):
        print(f"Error en el núcleo de email: {error}")
        self.status_label.configure(text=f"Error: {error}", text_color=PALETTE["error"])
        self._set_ui_state("normal")