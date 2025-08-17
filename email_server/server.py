import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.policy import SMTP

# Pasta onde estão os JSONs
PASTA_JSON = "./dados_alunos"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "@inf.ufpel.edu.br"
SMTP_PASS = ""

REMETENTE_PADRAO = f"UFPel <{SMTP_USER}>"

def enviar_email(remetente, destinatario_nome, destinatario_email, assunto, corpo_texto, corpo_html):
    msg = MIMEMultipart("alternative", policy=SMTP)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = f"{destinatario_nome} <{destinatario_email}>"

    msg.attach(MIMEText(corpo_texto, "plain", _charset="utf-8"))
    msg.attach(MIMEText(corpo_html, "html", _charset="utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    print(f"Email enviado para {destinatario_nome} <{destinatario_email}>")

def processar_jsons(pasta):
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".json")]
    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        enviar_email(
            remetente=dados.get("remetente", REMETENTE_PADRAO),
            destinatario_nome=dados["destinatario"],
            destinatario_email=dados["email_destinatario"],
            assunto=dados["assunto"],
            corpo_texto=dados["corpo_texto"],
            corpo_html=dados["corpo_html"]
        )

if __name__ == "__main__":
    processar_jsons(PASTA_JSON)