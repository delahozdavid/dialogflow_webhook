import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

#HOST (hostinger, gmail, etc...)
EMAIL_HOST = os.getenv('EMAIL_HOST')
#HOST PORT
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
#sender email
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
#sender password
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')



def send_email_with_file(subject, body, email_to_send_to, path_file):
    # print("llegie")
    file_path = os.getcwd() + "\\files\\" + path_file
    # respuesta = f"{EMAIL_HOST} {EMAIL_PORT} {EMAIL_HOST_USER} {subject} {body} {path_file} {current_file}"
    # return respuesta
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = EMAIL_HOST_USER
    message['To'] = email_to_send_to
    body_part = MIMEText(body)
    message.attach(body_part)
    with open(file_path,'rb') as file:
        # Attach the file with filename to the email
        message.attach(MIMEApplication(file.read(), Name=path_file))
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, email_to_send_to, message.as_string())
    # print("ya se cabo el metodo")
    return True
