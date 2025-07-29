import os
import re
import csv
from email import policy
from email.parser import BytesParser
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Configurações
DOMINIO_OFICIAL = "inf.ufpel.edu.br"
TEMPLATE_HTML_FRAG = "<!-- Template oficial UFPel -->"  # Exemplo, substitua pelo trecho real
QUARENTENA_DIR = "quarentena"
ALERTA_CSV = "alertas.csv"

# Inicializa GPT-2 para perplexity
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

def calcula_perplexity(texto):
    encodings = tokenizer(texto, return_tensors='pt')
    max_length = model.config.n_positions
    stride = 512
    nlls = []
    for i in range(0, encodings.input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = i + stride
        trg_len = end_loc - i
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs.loss * trg_len

        nlls.append(neg_log_likelihood)

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.item()

def extrai_links(texto):
    # regex simples para encontrar links http/https
    return re.findall(r'https?://[^\s">]+', texto)

def analisa_links(links):
    risco = 0.0
    for link in links:
        # Exemplo de regra simples: links que não contenham domínio oficial têm risco
        if DOMINIO_OFICIAL not in link:
            risco += 0.5
        # Pode adicionar checagens de links encurtados, IP no lugar de domínio etc.
    return min(risco, 1.0)

def verifica_template(html):
    # Checa se trecho do template oficial está presente
    return 0.0 if TEMPLATE_HTML_FRAG in html else 1.0  # 1.0 = risco máximo se não achar

def verifica_remetente(from_field):
    # Verifica se domínio do remetente é o esperado
    if from_field and DOMINIO_OFICIAL in from_field:
        return 0.0
    return 1.0

def calcula_score(perplexity, link_risk, template_risk, sender_risk):
    # Exemplo: normalize perplexity entre 0 e 50 (valores maiores = menos risco)
    # Inverte para risco: valores baixos perplexity = alto risco
    p_risk = max(0, min(1, (50 - perplexity) / 50))

    # Combina riscos (peso igual para exemplo)
    score = (p_risk + link_risk + template_risk + sender_risk) / 4
    return score

def salva_alerta(arquivo_eml, score):
    os.makedirs(QUARENTENA_DIR, exist_ok=True)
    destino = os.path.join(QUARENTENA_DIR, os.path.basename(arquivo_eml))
    os.rename(arquivo_eml, destino)

    # Grava alerta CSV
    existe = os.path.isfile(ALERTA_CSV)
    with open(ALERTA_CSV, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not existe:
            writer.writerow(['arquivo', 'score'])
        writer.writerow([os.path.basename(arquivo_eml), score])
    print(f"Email {arquivo_eml} colocado em quarentena com score {score:.2f}")

def analisa_email(caminho_eml):
    with open(caminho_eml, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    from_field = msg['From']
    if msg.is_multipart():
        partes = [part.get_content() for part in msg.walk() if part.get_content_type() == 'text/plain']
        texto = "\n".join(partes)
        partes_html = [part.get_content() for part in msg.walk() if part.get_content_type() == 'text/html']
        html = "\n".join(partes_html)
    else:
        texto = msg.get_content()
        html = ""  # sem html

    links = extrai_links(texto + " " + html)
    link_risk = analisa_links(links)
    template_risk = verifica_template(html)
    sender_risk = verifica_remetente(from_field)
    perplexity = calcula_perplexity(texto)

    score = calcula_score(perplexity, link_risk, template_risk, sender_risk)

    print(f"Email: {caminho_eml}")
    print(f"Perplexity: {perplexity:.2f}")
    print(f"Link risk: {link_risk:.2f}, Template risk: {template_risk:.2f}, Sender risk: {sender_risk:.2f}")
    print(f"Score final de risco: {score:.2f}")

    if score > 0.5:
        salva_alerta(caminho_eml, score)

def main(pasta_emails):
    arquivos = [os.path.join(pasta_emails, f) for f in os.listdir(pasta_emails) if f.endswith('.eml')]
    for arquivo in arquivos:
        analisa_email(arquivo)

if __name__ == "__main__":
    pasta_emails = "./emails"  # Coloque seus .eml aqui
    main(pasta_emails)
