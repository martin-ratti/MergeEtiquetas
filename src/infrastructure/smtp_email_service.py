# src/infrastructure/smtp_email_service.py
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from typing import Dict
from src.core.interfaces import IEmailService
from pathlib import Path

from src.core.exceptions import EmailError

class SMTPEmailService(IEmailService):
    """
    Implementación concreta de IEmailService usando smtplib de Python.
    
    Se especializa en conectarse a Gmail y enviar un adjunto.
    """

    def send_email_with_attachment(self, config: Dict[str, str], file_path: str) -> None:
        """
        Envía un email con un archivo adjunto usando Gmail.
        
        Args:
            config (Dict[str, str]): Diccionario con credenciales y destinatario.
            file_path (str): Ruta al archivo que se debe adjuntar.
            
        Raises:
            EmailError: Si falla la conexión, autenticación o envío.
        """
        
        # Crear el objeto del mensaje
        msg = EmailMessage()
        msg['Subject'] = config['ASUNTO']
        msg['From'] = config['EMAIL_EMISOR']
        msg['To'] = config['EMAIL_RECEPTOR']
        msg.set_content("Adjunto se encuentra el PDF de etiquetas generado.")

        # Adjuntar el archivo PDF
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = Path(file_path).name
                msg.add_attachment(file_data, 
                                   maintype="application", 
                                   subtype="octet-stream", 
                                   filename=file_name)
        except Exception as e:
            raise EmailError(f"Error al leer el archivo adjunto: {e}")

        # Enviar el correo usando un contexto SSL seguro
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(config['EMAIL_EMISOR'], config['APP_PASSWORD'])
                server.send_message(msg)
                
        except smtplib.SMTPAuthenticationError:
            raise EmailError(
                "Error de autenticación. Revisa EMAIL_EMISOR o APP_PASSWORD en config.ini"
            )
        except smtplib.SMTPServerDisconnected:
            raise EmailError("Se perdió la conexión con el servidor de Google.")
        except Exception as e:
            raise EmailError(f"Error desconocido al enviar el email: {e}")
