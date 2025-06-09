import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def enviar_correo(destinatario, asunto, mensaje, pdf_enviar):
    # Configuración del servidor SMTP de Gmail
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    correo_origen = 'eventhub.oficial@gmail.com'
    contraseña = 'koxp cydb hltk ttxj'  # Contraseña de aplicación

    # Crear el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = correo_origen
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Adjuntar el PDF si se proporciona
    if pdf_enviar:
        pdf_enviar.seek(0)  # Asegurarse de estar al inicio del buffer
        parte = MIMEBase('application', 'pdf')
        parte.set_payload(pdf_enviar.read())
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', 'attachment', filename='ticket.pdf')
        msg.attach(parte)

    try:
        # Conectarse al servidor SMTP y enviar el correo
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()  # Iniciar conexión segura
        servidor.login(correo_origen, contraseña)
        servidor.sendmail(correo_origen, destinatario, msg.as_string())
        print(f"Correo enviado a {destinatario} con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        servidor.quit()  # Cerrar conexión
