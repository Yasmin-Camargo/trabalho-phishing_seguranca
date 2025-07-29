import dkim
import smtplib

def sign_email(raw_email_bytes, selector, domain, private_key_path):
    with open(private_key_path, 'rb') as f:
        private_key = f.read()

    signature = dkim.sign(
        message=raw_email_bytes,
        selector=selector.encode(),
        domain=domain.encode(),
        privkey=private_key,
        include_headers=[b"From", b"To", b"Subject", b"Date"]
    )
    return signature + raw_email_bytes

def send_signed_email(signed_email_bytes, sender, recipients, smtp_host='localhost', smtp_port=1025):
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.sendmail(sender, recipients, signed_email_bytes)

if __name__ == "__main__":
    # Ler email raw
    with open("email.txt", "rb") as f:
        raw_email = f.read()

    # Assinar
    signed_email = sign_email(raw_email, "default", "inf.ufpel.edu.br", "dkim_keys/private.key")

    # Salvar email assinado
    with open("email_signed.txt", "wb") as f:
        f.write(signed_email)

    print("E-mail assinado com DKIM e salvo em 'email_signed.txt'")

    # Enviar para MailHog
    send_signed_email(
        signed_email_bytes=signed_email,
        sender="seu_email@inf.ufpel.edu.br"a,
        recipients=["destinatario@inf.ufpel.edu.br"],
        smtp_host="localhost",
        smtp_port=1025
    )

    print("E-mail assinado enviado para MailHog.")
