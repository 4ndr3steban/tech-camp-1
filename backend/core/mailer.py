from settings import settings
from schemas.mailbody import MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP


def send_mail(data: MailBody | None = None):
    """ Envía un correo electrónico con los datos proporcionados.

    Args:
    - `data` (MailBody): Datos del correo electrónico.

    Returns:
    """
    
    msg = MailBody(to=data.to, subject=data.subject, body=data.body)

    # Crear el objeto mensaje y agregarle el cuerpo
    message = MIMEText(msg.body, "html")
    message["From"] = settings.MAILUSERNAME
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        # Crear una conexión SMTP
        with SMTP(settings.HOST, settings.PORT) as server:
            server.ehlo()
            # Iniciar la conexión
            server.starttls(context=ctx)
            server.ehlo()
            # Iniciar sesión en el servidor SMTP
            server.login(settings.MAILUSERNAME, settings.PASSWORD)
            # Enviar el correo electrónico
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}