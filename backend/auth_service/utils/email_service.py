# auth_service/utils/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
    """
    Envia um e-mail simples em formato texto via SMTP (TLS).
    Retorna True se enviado com sucesso.
    """
    try:
        # Configurações do .env
        smtp_server = os.getenv("EMAIL_HOST")
        smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        usuario = os.getenv("EMAIL_USERNAME")
        senha = os.getenv("EMAIL_PASSWORD")
        remetente = os.getenv("EMAIL_FROM", usuario)

        # Criação do e-mail
        mensagem = MIMEMultipart()
        mensagem["From"] = remetente
        mensagem["To"] = destinatario
        mensagem["Subject"] = assunto
        mensagem.attach(MIMEText(corpo, "plain"))

        # Conexão e envio
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(usuario, senha)
            servidor.send_message(mensagem)

        print(f"[✓] E-mail enviado para: {destinatario}")
        return True

    except Exception as e:
        print(f"[✗] Erro ao enviar e-mail: {e}")
        return False
