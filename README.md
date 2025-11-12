
```markdown
# 🏷️ MergeEtiquetas (Fusionador de Etiquetas)

**MergeEtiquetas** es una aplicación de escritorio ligera, construida en Python, diseñada para la forrajería "Animall". Su única misión es eliminar el trabajo manual de fusionar múltiples archivos PDF de etiquetas en un solo documento listo para imprimir.

La aplicación escanea automáticamente una estructura de carpetas, permitiendo al usuario seleccionar etiquetas individuales o categorías enteras, y genera un único PDF fusionado con un solo clic.

![Captura de pantalla de la aplicación MergeEtiquetas](httpsimg/screenshot.png)
*(Recomendación: Reemplaza esta línea creando una carpeta `img` y guardando una captura de pantalla de la app llamada `screenshot.png` allí)*

---

## 🚀 Características Principales

* **Detección Automática de Categorías:** Simplemente crea carpetas en `_ETIQUETAS_PDFS/`. La aplicación las detectará y las usará como categorías.
* **Selección Rápida:** Marca etiquetas individuales o usa la casilla "Seleccionar Todos" para añadir categorías enteras de una sola vez.
* **Interfaz Interactiva:**
    * **Botón Inteligente:** El botón "Generar" se activa solo si hay etiquetas seleccionadas y muestra un recuento en tiempo real.
    * **Tarjetas Interactivas:** Cada categoría se ilumina al pasar el ratón por encima.
* **Limpieza Automática:** Después de generar un PDF, la selección se limpia automáticamente, dejando la app lista para la siguiente tarea.
* **Acceso Rápido:** Un diálogo de éxito te pregunta si deseas abrir la carpeta de salida inmediatamente.
* **Ultra-Ligera:** Construida con `CustomTkinter` y `PyMuPDF` (un wrapper de C), la aplicación es extremadamente rápida y consume muy pocos recursos.

---

## 🛠️ Modo de Uso (Para el Usuario Final)

Este programa está diseñado para ser portátil. Puedes mover la carpeta `Animall Fusionador` a cualquier lugar (otro PC, un pendrive, etc.) siempre que mantengas esta estructura:

```

/Animall Fusionador
├── MergeEtiquetas.exe       \<-- El programa
├── \_ETIQUETAS\_PDFS/         \<-- ¡Aquí pones tus PDFs\!
├── \_SALIDA/                 \<-- Aquí se guardan los resultados
└── logo.png                 \<-- (Requerido por el .exe)

````

1.  **Añadir Etiquetas:** Arrastra tus archivos `.pdf` de etiquetas dentro de la carpeta `_ETIQUETAS_PDFS/`. Puedes organizarlos en subcarpetas (ej. `.../Jabones/`, `.../Perfuminas/`).
2.  **Ejecutar:** Haz doble clic en `MergeEtiquetas.exe`.
3.  **Seleccionar:** Usa las casillas para seleccionar las etiquetas que quieres imprimir.
4.  **Generar:** Haz clic en el botón "Generar PDF...".
5.  **Listo:** El archivo final (`etiquetas_imprimir.pdf`) aparecerá en la carpeta `_SALIDA/`.

---

## 🧑‍💻 Para Desarrolladores

Esta aplicación sigue los principios de **Clean Architecture** para asegurar que sea mantenible, testeable y escalable.

* `src/core`: Lógica de negocio pura (agnóstica).
* `src/infrastructure`: Implementaciones concretas (PyMuPDF).
* `src/interface`: La GUI (CustomTkinter) y el manejo de estado.

### Configuración del Entorno

1.  Clona el repositorio.
2.  Crea un entorno virtual:
    ```bash
    python -m venv venv
    ```
3.  Activa el entorno:
    ```bash
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
4.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
5.  Ejecuta la aplicación en modo desarrollo:
    ```bash
    python main.py
    ```

### 📦 Creación del Ejecutable (`.exe`)

Usamos `PyInstaller` para empaquetar la aplicación en un solo ejecutable.

1.  Asegúrate de que `logo.png` esté en la raíz del proyecto.
2.  Ejecuta el siguiente comando (con el `venv` activo):

    ```powershell
    # Comando para Windows
    pyinstaller --onefile --windowed --add-data="logo.png;." main.py --name="MergeEtiquetas"
    ```

3.  El ejecutable final aparecerá en la carpeta `dist/`.
4.  Para la distribución final, sigue las instrucciones de "Modo de Uso" (copia el `.exe` a una carpeta limpia junto con `_ETIQUETAS_PDFS/` y `_SALIDA/`).
````

-----

