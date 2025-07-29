import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from red_team.templates import get_default_plain_text, get_cobalto_html_body


def build_email_message(to_name, to_email, subject, plain_text=None, html_body=None):
    plain_text = plain_text or get_default_plain_text()
    html_body = html_body or get_cobalto_html_body(plain_text)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'[cobalto] {subject}'
    msg['From'] = 'UFPel <no-reply@ufpel.edu.br>'
    msg['To'] = f'{to_name} <{to_email}>'
    msg['Reply-To'] = 'coordenacao.projetos.ufpel@gmail.com'
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain="ufpel.edu.br")
    msg['MIME-Version'] = '1.0'

    msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    return msg


def send_email(to_name="USER", to_email="user@ufpel.edu.br",
               subject="Meeting on June 27 at 17:10",
               plain_text=None, html_body=None):
    smtp_host = 'localhost'
    smtp_port = 1025

    msg = build_email_message(to_name, to_email, subject, plain_text, html_body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.send_message(msg)

    print("HTML email sent successfully!")


if __name__ == "__main__":
    send_email()
