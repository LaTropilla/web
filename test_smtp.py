import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Información de configuración
smtp_server = 'mail.turismolatropilla.cl'
smtp_port = 465  # Puerto para SSL
smtp_user = 'noreply@turismolatropilla.cl'
smtp_password = 'Tr0p1ll41!'

# Configuración del correo
from_address = 'noreply@turismolatropilla.cl'
to_address = 'elmatiiix22@gmail.com'  # Cambia esto a la dirección del destinatario
subject = 'Correo de Prueba'
body = 'Este es el cuerpo del correo de prueba.'

# Crear el mensaje
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Enviar el correo
try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # Usar SMTP_SSL para SSL
    server.login(smtp_user, smtp_password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
    print('Correo enviado exitosamente')
except Exception as e:
    print(f'Error al enviar el correo: {e}')
