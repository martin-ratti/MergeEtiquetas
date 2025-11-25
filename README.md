<h1 align="center">🏷️ MergeEtiquetas - Animall Forrajería</h1>

<div align="center">
    <img src="https://img.shields.io/badge/Estado-Producción-success?style=for-the-badge&logo=check&logoColor=white" alt="Estado Badge"/>
    <img src="https://img.shields.io/badge/Versión-1.0.0-blue?style=for-the-badge" alt="Version Badge"/>
</div>

<p align="center">
    <a href="https://github.com/martin-ratti" target="_blank" style="text-decoration: none;">
        <img src="https://img.shields.io/badge/👤%20Martín%20Ratti-martin--ratti-000000?style=for-the-badge&logo=github&logoColor=white" alt="Martin"/>
    </a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows Badge"/>
    <img src="https://img.shields.io/badge/GUI-CustomTkinter-2B2B2B?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter Badge"/>
    <img src="https://img.shields.io/badge/PDF-PyMuPDF-FF6F00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PDF Badge"/>
    <img src="https://img.shields.io/badge/Mail-SMTP%20Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail Badge"/>
</p>

<hr>

<h2>🎯 Objetivo y Alcance</h2>

<p>
    <strong>MergeEtiquetas</strong> es una aplicación de escritorio robusta y ligera desarrollada a medida para 
    <strong>Animall Forrajería</strong>. Su misión crítica es eliminar el trabajo manual de procesamiento de etiquetas.
</p>

<p>
    El sistema escanea automáticamente una estructura de carpetas predefinida, permite al usuario seleccionar 
    etiquetas individuales o categorías completas mediante una interfaz gráfica moderna, fusiona los archivos PDF 
    en un documento listo para imprimir y, opcionalmente, lo distribuye por correo electrónico.
</p>

<hr>

<h2>⚙️ Stack Tecnológico & Arquitectura</h2>

<p>El proyecto sigue los principios de <strong>Clean Architecture</strong> para asegurar desacoplamiento y escalabilidad.</p>

<table>
 <thead>
  <tr>
   <th>Capa / Componente</th>
   <th>Tecnología / Ruta</th>
   <th>Descripción</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><strong>Interface (GUI)</strong></td>
   <td><code>src/interface/</code> (CustomTkinter)</td>
   <td>Capa de presentación. Maneja la ventana, eventos, tarjetas interactivas y feedback visual.</td>
  </tr>
  <tr>
   <td><strong>Core (Dominio)</strong></td>
   <td><code>src/core/</code> (Python Puro)</td>
   <td>Lógica de negocio agnóstica. Define casos de uso (Fusionar, Enviar) e Interfaces.</td>
  </tr>
  <tr>
   <td><strong>Infrastructure</strong></td>
   <td><code>src/infrastructure/</code></td>
   <td>Implementaciones concretas: <strong>PyMuPDF</strong> (para PDFs) y <strong>smtplib</strong> (para Email).</td>
  </tr>
  <tr>
   <td><strong>Empaquetado</strong></td>
   <td>PyInstaller</td>
   <td>Generación del ejecutable <code>.exe</code> portable (single-file).</td>
  </tr>
 </tbody>
</table>

<hr>

<h2>🚀 Características Principales</h2>

<ul>
    <li><strong>⚡ Automatización de PDFs</strong>: Fusión inteligente de múltiples archivos en un solo <code>etiquetas_imprimir.pdf</code> optimizado.</li>
    <li><strong>📂 Detección Dinámica</strong>: Escaneo automático de carpetas en <code>_ETIQUETAS_PDFS/</code> para crear categorías al instante.</li>
    <li><strong>📧 Conectividad SMTP</strong>: Envío automático del reporte generado a sucursales o proveedores vía Gmail.</li>
    <li><strong>🎨 UX/UI Moderna</strong>: 
        <ul>
            <li>Modo oscuro nativo.</li>
            <li>Tarjetas interactivas con efectos <em>hover</em>.</li>
            <li>Botón de acción inteligente con contador en tiempo real.</li>
        </ul>
    </li>
</ul>

<hr>

<h2>🛠️ Modo de Uso (Portable)</h2>

<p>La aplicación está diseñada para ser <strong>"Plug & Play"</strong>. La estructura de carpetas debe mantenerse así:</p>

<pre>
/Animall Fusionador
├── MergeEtiquetas.exe       <-- El programa compilado
├── config.ini               <-- Configuración de Email (Opcional)
├── logo.png                 <-- Recurso gráfico (Requerido)
├── _ETIQUETAS_PDFS/         <-- ¡Tus carpetas con PDFs van aquí!
│   ├── Jabones/
│   ├── Perfuminas/
│   └── ...
└── _SALIDA/                 <-- Aquí aparecerá el PDF final
</pre>

<h3>Pasos de Ejecución</h3>
<ol>
    <li><strong>Cargar:</strong> Arrastra tus archivos <code>.pdf</code> dentro de las carpetas en <code>_ETIQUETAS_PDFS</code>.</li>
    <li><strong>Ejecutar:</strong> Abre <code>MergeEtiquetas.exe</code>.</li>
    <li><strong>Seleccionar:</strong> Marca las etiquetas deseadas o usa "Seleccionar Todos" por categoría.</li>
    <li><strong>Procesar:</strong>
        <ul>
            <li>Clic en <strong>"Generar PDF"</strong> para crear el archivo en <code>_SALIDA/</code>.</li>
            <li>Clic en <strong>"Enviar PDF por Email"</strong> (si está configurado) para despacharlo.</li>
        </ul>
    </li>
</ol>

<hr>

<h2>⚙️ Configuración del Email</h2>

<p>Para habilitar el botón de envío, crea/edita el archivo <code>config.ini</code> junto al ejecutable:</p>

<table>
 <thead>
  <tr>
   <th>Archivo</th>
   <th>Contenido Requerido</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><code>config.ini</code></td>
   <td>
<pre lang="ini">
[Email]
email_emisor = tu_correo@gmail.com
app_password = xxxx xxxx xxxx xxxx
email_receptor = destino@ejemplo.com
asunto = Pedido de Etiquetas - Animall
</pre>
   </td>
  </tr>
 </tbody>
</table>
<p><em>Nota: La <code>app_password</code> se genera desde la configuración de seguridad de Google.</em></p>

<hr>

<h2>🧑‍💻 Setup para Desarrolladores</h2>

<h3>1. Inicialización</h3>
<pre><code># Clonar repositorio
git clone https://github.com/martin-ratti/MergeEtiquetas.git

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
</code></pre>

<h3>2. Ejecución en Dev</h3>
<pre><code>python main.py</code></pre>

<h3>3. Compilación (Build .exe)</h3>
<p>Comando para generar el ejecutable final con todos los recursos embebidos:</p>
<pre><code>pyinstaller --onefile --windowed --add-data="logo.png;." --icon=logo.png main.py --name="MergeEtiquetas"</code></pre>

<hr>

<h2>⚖️ Créditos</h2>

<p>
    Desarrollado por <strong>Martín Ratti</strong> para uso interno en Animall Forrajería.
</p>
