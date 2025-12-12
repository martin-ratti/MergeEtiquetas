<div align="center">

# 🏷️ MergeEtiquetas - Animall Forrajería

<img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
<img src="https://img.shields.io/badge/Versión-1.0.0-blue?style=for-the-badge" alt="Version Badge"/>
<img src="https://img.shields.io/badge/Licencia-Proprietary-red?style=for-the-badge" alt="License Badge"/>

<br/>

<a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
</a>

<br/>

<p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Arquitectura-Clean%20Arch-orange?style=for-the-badge&logo=expertsexchange&logoColor=white" alt="Clean Arch Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/PDF-PyMuPDF-FF6F00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PyMuPDF Badge"/>
    <img src="https://img.shields.io/badge/Mail-SMTP%20Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail Badge"/>
</p>

</div>

---

## 🎯 Objetivo y Alcance

**MergeEtiquetas** es una aplicación de escritorio robusta desarrollada a medida para **Animall Forrajería**. Su misión crítica es eliminar el trabajo manual de procesamiento e impresión de etiquetas de precios.

El sistema escanea automáticamente una estructura de carpetas predefinida, permite al usuario seleccionar etiquetas individuales o categorías completas mediante una interfaz gráfica moderna, fusiona los archivos PDF en un documento listo para imprimir y automatiza su distribución por correo electrónico.

---

## 🏛️ Arquitectura y Diseño

El proyecto sigue estrictamente los principios de **Clean Architecture**, utilizando **Inyección de Dependencias** en el punto de entrada (`main.py`) para desacoplar la interfaz gráfica de la lógica de negocio y la infraestructura.

### Diagrama de Flujo de Datos

| Capa | Componente | Responsabilidad |
| :--- | :--- | :--- |
| **Interface** | `src/interface/app_gui.py` | Gestiona la interacción visual, el estado de los checkboxes y feedback al usuario. |
| **Core** | `src/core/use_cases.py` | Orquesta la lógica: valida entradas y coordina los puertos (Interfaces). |
| **Infrastructure** | `src/infrastructure/` | Implementación técnica: Manipulación de bytes PDF (`PyMuPDF`) y comunicación con servidores de correo (`smtplib`). |

-----

## 🚀 Características Principales

  * **⚡ Automatización de PDFs:** Fusión inteligente de múltiples archivos en un solo `etiquetas_imprimir.pdf` optimizado usando el motor `fitz` (PyMuPDF).
  * **📂 Escaneo Dinámico:** La interfaz se construye dinámicamente leyendo la estructura de carpetas en `_ETIQUETAS_PDFS/`. Si agregas una carpeta nueva, aparece mágicamente en la App.
  * **📧 Conectividad SMTP:** Envío automático del reporte generado a sucursales o proveedores vía Gmail con seguridad SSL.
  * **🎨 UX/UI Moderna:**
      * Modo oscuro nativo ("Dark Mode").
      * Tarjetas interactivas con selección "Padre/Hijo" (seleccionar toda una categoría o etiquetas sueltas).
      * Validación de estado (el botón de envío solo se activa si hay configuración y PDF generado).

-----

## 🛠️ Modo de Uso (Portable)

La aplicación está diseñada para ser **"Plug & Play"**. La estructura de carpetas debe mantenerse así para que el autodescubrimiento funcione:

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
```

### Pasos de Ejecución

1.  **Cargar:** Arrastra tus archivos `.pdf` dentro de las carpetas correspondientes en `_ETIQUETAS_PDFS`.
2.  **Ejecutar:** Abre `MergeEtiquetas.exe`.
3.  **Seleccionar:** Marca las etiquetas deseadas o usa "Seleccionar Todos" por categoría.
4.  **Procesar:**
      * Clic en **"Generar PDF"** para crear el archivo fusionado en `_SALIDA/`.
      * Clic en **"Enviar PDF por Email"** (se habilita tras generar) para despacharlo.

-----

## ⚙️ Configuración del Email

Para habilitar el botón de envío, crea o edita el archivo `config.ini` junto al ejecutable. Si este archivo no existe o está incompleto, la función de email se deshabilitará automáticamente.

**Contenido de `config.ini`:**

```ini
[Email]
email_emisor = tu_correo@gmail.com
# Generar contraseña de aplicación en: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
app_password = xxxx xxxx xxxx xxxx
email_receptor = destino@ejemplo.com
asunto = Pedido de Etiquetas - Animall
```

-----

## 🧑‍💻 Setup para Desarrolladores

Si deseas contribuir o compilar tu propia versión:

### 1\. Configuración del Entorno

```bash
# Clonar repositorio
git clone [https://github.com/martin-ratti/MergeEtiquetas.git](https://github.com/martin-ratti/MergeEtiquetas.git)

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2\. Ejecución en Desarrollo

```bash
python main.py
```

### 3\. Compilación (Build .exe)

El proyecto usa `PyInstaller` para empaquetar todo (código + logo) en un solo archivo.

```bash
pyinstaller --onefile --windowed --add-data="logo.png;." --icon=logo.png main.py --name="MergeEtiquetas"
```

-----

## ⚖️ Créditos

Desarrollado por **Martín Ratti** para uso interno en Animall Forrajería.

