"""
Utilitário para envio de e-mails usando SMTP + TLS.
Compatível com Gmail, Outlook, etc.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
    """
    Envia um e-mail em formato texto para o destinatário.
    Requer variáveis definidas no ambiente do container.

    Returns:
        bool: True se enviado, False se erro
    """

    smtp_host = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT", "587"))
    usuario = os.getenv("EMAIL_USERNAME")
    senha = os.getenv("EMAIL_PASSWORD")
    remetente = os.getenv("EMAIL_FROM", usuario)

    # Verificação obrigatória
    if not smtp_host or not usuario or not senha:
        logger.error("❌ Configuração SMTP incompleta.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(usuario, senha)
            smtp.send_message(msg)

        logger.info(f"✅ E-mail enviado para: {destinatario}")
        return True

    except Exception as e:
        logger.error(f"✖️ Erro ao enviar e-mail: {e}")
        return False
