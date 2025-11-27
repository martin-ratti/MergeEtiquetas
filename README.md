<div align="center">

# 🏷️ MergeEtiquetas - Animall Forrajería

<img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-1.0.0-blue?style=for-the-badge" alt="Version Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/PDF-PyMuPDF-FF6F00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PDF Badge"/>
    <img src="https://img.shields.io/badge/Mail-SMTP%20Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

**MergeEtiquetas** es una aplicación de escritorio robusta y ligera desarrollada a medida para **Animall Forrajería**. Su misión crítica es eliminar el trabajo manual de procesamiento de etiquetas.

El sistema escanea automáticamente una estructura de carpetas predefinida, permite al usuario seleccionar etiquetas individuales o categorías completas mediante una interfaz gráfica moderna, fusiona los archivos PDF en un documento listo para imprimir y, opcionalmente, lo distribuye por correo electrónico.

---

## ⚙️ Stack Tecnológico & Arquitectura

El proyecto sigue los principios de **Clean Architecture** para asegurar desacoplamiento y escalabilidad.

| Capa / Componente | Tecnología / Ruta | Descripción |
| :--- | :--- | :--- |
| **Interface (GUI)** | `src/interface/`<br>_(CustomTkinter)_ | Capa de presentación. Maneja la ventana, eventos, tarjetas interactivas y feedback visual. |
| **Core (Dominio)** | `src/core/`<br>_(Python Puro)_ | Lógica de negocio agnóstica. Define casos de uso (Fusionar, Enviar) e Interfaces. |
| **Infrastructure** | `src/infrastructure/` | Implementaciones concretas: **PyMuPDF** (para PDFs) y **smtplib** (para Email). |
| **Empaquetado** | PyInstaller | Generación del ejecutable `.exe` portable (single-file). |

---

## 🚀 Características Principales

* **⚡ Automatización de PDFs:** Fusión inteligente de múltiples archivos en un solo `etiquetas_imprimir.pdf` optimizado.
* **📂 Detección Dinámica:** Escaneo automático de carpetas en `_ETIQUETAS_PDFS/` para crear categorías al instante.
* **📧 Conectividad SMTP:** Envío automático del reporte generado a sucursales o proveedores vía Gmail.
* **🎨 UX/UI Moderna:**
    * Modo oscuro nativo.
    * Tarjetas interactivas con efectos *hover*.
    * Botón de acción inteligente con contador en tiempo real.

---

## 🛠️ Modo de Uso (Portable)

La aplicación está diseñada para ser **"Plug & Play"**. La estructura de carpetas debe mantenerse así:

```text
/Animall Fusionador
├── MergeEtiquetas.exe       <-- El programa compilado
├── config.ini               <-- Configuración de Email (Opcional)
├── logo.png                 <-- Recurso gráfico (Requerido)
├── _ETIQUETAS_PDFS/         <-- ¡Tus carpetas con PDFs van aquí!
│   ├── Jabones/
│   ├── Perfuminas/
│   └── ...
└── _SALIDA/                 <-- Aquí aparecerá el PDF final
````

### Pasos de Ejecución

1.  **Cargar:** Arrastra tus archivos `.pdf` dentro de las carpetas en `_ETIQUETAS_PDFS`.
2.  **Ejecutar:** Abre `MergeEtiquetas.exe`.
3.  **Seleccionar:** Marca las etiquetas deseadas o usa "Seleccionar Todos" por categoría.
4.  **Procesar:**
      * Clic en **"Generar PDF"** para crear el archivo en `_SALIDA/`.
      * Clic en **"Enviar PDF por Email"** (si está configurado) para despacharlo.

-----

## ⚙️ Configuración del Email

Para habilitar el botón de envío, crea/edita el archivo `config.ini` junto al ejecutable:

| Archivo | Contenido Requerido |
| :--- | :--- |
| `config.ini` | Ver bloque de código abajo |

```ini
[Email]
email_emisor = tu_correo@gmail.com
app_password = xxxx xxxx xxxx xxxx
email_receptor = destino@ejemplo.com
asunto = Pedido de Etiquetas - Animall
```

> **Nota:** La `app_password` se genera desde la configuración de seguridad de Google (App Passwords).

-----

## 🧑‍💻 Setup para Desarrolladores

### 1\. Inicialización

```bash
# Clonar repositorio
git clone [https://github.com/martin-ratti/MergeEtiquetas.git](https://github.com/martin-ratti/MergeEtiquetas.git)

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2\. Ejecución en Dev

```bash
python main.py
```

### 3\. Compilación (Build .exe)

Comando para generar el ejecutable final con todos los recursos embebidos:

```bash
pyinstaller --onefile --windowed --add-data="logo.png;." --icon=logo.png main.py --name="MergeEtiquetas"
```

-----

## ⚖️ Créditos

Desarrollado por **Martín Ratti** para uso interno en Animall Forrajería.
