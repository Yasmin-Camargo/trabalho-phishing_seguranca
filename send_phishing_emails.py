#!/usr/bin/env python3
import json
import os
import sys
import glob
from datetime import datetime
from email_server.server import send_email

def send_phishing_emails_from_folder():
    emails_folder = "red-team/emails_phishing"
    log_file = f"log_envio_phishing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if not os.path.exists(emails_folder):
        print(f"Erro: Pasta {emails_folder} não encontrada!")
        return
    
    email_files = glob.glob(os.path.join(emails_folder, "*.json"))
    
    if not email_files:
        print(f"Nenhum arquivo de email encontrado em {emails_folder}")
        return
    
    print(f"Encontrados {len(email_files)} emails para enviar...")
    
    resultados = []
    emails_enviados = 0
    emails_com_erro = 0
    
    for email_file in email_files:
        try:
            # Carregar dados do email
            with open(email_file, 'r', encoding='utf-8') as f:
                email_data = json.load(f)
            
            # Extrair informações necessárias
            destinatario = email_data.get('destinatario', 'Destinatário')
            email_destinatario = email_data.get('email_destinatario', '')
            assunto = email_data.get('assunto', 'Sem assunto')
            remetente = email_data.get('remetente', 'Remetente')
            corpo_texto = email_data.get('corpo_texto', '')
            corpo_html = email_data.get('corpo_html', None)
            
            if not email_destinatario:
                print(f"Erro: Email destinatário não encontrado em {email_file}")
                emails_com_erro += 1
                continue
            
            # Enviar email
            send_email(
                to_name=destinatario,
                to_email=email_destinatario,
                subject=assunto,
                plain_text=corpo_texto,
                html_body=corpo_html
            )
            
            print(f"✓ Enviado para {destinatario} ({email_destinatario})")
            emails_enviados += 1
            
            # Registrar no log
            resultados.append({
                "arquivo": os.path.basename(email_file),
                "nome": destinatario,
                "email": email_destinatario,
                "assunto": assunto,
                "remetente": remetente,
                "status": "enviado",
                "timestamp": datetime.now().isoformat()
            })
            
        except json.JSONDecodeError as e:
            print(f"✗ Erro ao ler JSON em {email_file}: {e}")
            emails_com_erro += 1
            resultados.append({
                "arquivo": os.path.basename(email_file),
                "nome": "ERRO",
                "email": "ERRO",
                "assunto": "ERRO",
                "remetente": "ERRO",
                "status": f"erro_json: {e}",
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"✗ Erro ao enviar email de {email_file}: {e}")
            emails_com_erro += 1
            resultados.append({
                "arquivo": os.path.basename(email_file),
                "nome": email_data.get('destinatario', 'ERRO'),
                "email": email_data.get('email_destinatario', 'ERRO'),
                "assunto": email_data.get('assunto', 'ERRO'),
                "remetente": email_data.get('remetente', 'ERRO'),
                "status": f"erro_envio: {e}",
                "timestamp": datetime.now().isoformat()
            })
    
    # Salvar log em CSV
    import csv
    with open(log_file, mode="w", newline='', encoding="utf-8") as f:
        if resultados:
            fieldnames = resultados[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(resultados)

if __name__ == "__main__":
    send_phishing_emails_from_folder()
