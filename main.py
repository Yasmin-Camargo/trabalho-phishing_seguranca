import csv
import json
import os
import sys
from datetime import datetime
from email_server.server import send_email

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'red_team'))
import templates


CONTATOS_CSV = "contatos.csv"
LOG_ENVIO_CSV = f"log_envio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def gerar_e_enviar_emails():
    resultados = []

    with open(CONTATOS_CSV, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for contato in reader:
            nome = contato.get("nome")
            email = contato.get("email")

            phishing_data = templates.generate_phishing_email()
            if not phishing_data:
                print(f"Erro ao gerar e-mail para {nome} ({email})")
                continue
            
            email_data = json.loads(phishing_data)

            corpo_email = email_data['email'].replace("{name}", nome).replace("{email}", email)

            send_email(
                plain_text=corpo_email,
                subject=email_data['subject'],
                to_name=nome,
                to_email=email
            )

            print(f"Enviado para {nome} ({email})")

            resultados.append({
                "nome": nome,
                "email": email,
                "assunto": email_data['subject'],
                "remetente_falso": email_data['fake_sender_name'],
                "email_falso": email_data['email'],
                "corpo": corpo_email
            })

    with open(LOG_ENVIO_CSV, mode="w", newline='', encoding="utf-8") as f:
        fieldnames = ["nome", "email", "assunto", "remetente_falso", "email_falso", "corpo"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resultados)

    print(f"Log salvo em: {LOG_ENVIO_CSV}")


if __name__ == "__main__":
    gerar_e_enviar_emails()
