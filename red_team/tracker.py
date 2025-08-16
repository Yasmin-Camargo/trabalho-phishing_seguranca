from flask import Flask, request, render_template_string, url_for
import csv
import datetime
import os

app = Flask(__name__)
LOG_FILE = "cliques.csv"

# Garantir que a pasta 'red_team' seja usada como static
app.static_folder = os.path.dirname(os.path.abspath(__file__))

ALERTA_HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Alerta de Phishing</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #f8d7da; 
            color: #721c24; 
            text-align: center; 
            padding: 50px; 
        }
        .container { 
            border: 2px solid #f5c6cb; 
            background: #f8d7da; 
            padding: 30px; 
            border-radius: 10px; 
            display: inline-block; 
            max-width: 600px;
        }
        h1 { 
            font-size: 2em; 
            margin: 20px 0 10px 0; 
        }
        h2 { 
            font-size: 1.5em; 
            margin-bottom: 15px; 
        }
        p { 
            font-size: 1em; 
            margin: 10px 0; 
        }
        .emoji { 
            font-size: 3em; 
            margin-bottom: 10px;
        }
        img { 
            max-width: 300px; 
            margin: 20px 0; 
            border-radius: 10px; 
        }
        .descricao { 
            background-color: #f5c6cb; 
            color: #721c24; 
            padding: 15px; 
            border-radius: 8px; 
            margin-top: 20px; 
            text-align: left; 
            font-size: 0.9em; 
            line-height: 1.4em;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="{{ url_for('static', filename='gato_rindo.png') }}" alt="Gato rindo">
        <h1> CAIU NO PHISHING</h1>
        <p>Você clicou em um link de phishing simulado</p>
        <div class="descricao">
            <p><strong>O que é phishing:</strong> Phishing é um tipo de ataque cibernético em que criminosos tentam enganar usuários para que revelem informações confidenciais, como senhas, dados bancários ou números de cartão de crédito. Eles geralmente se passam por entidades legítimas, como bancos ou empresas, por meio de e-mails, mensagens ou sites falsos. O objetivo é roubar essas informações para fins fraudulentos.</p>
            <p>Este é um teste educacional para conscientização em segurança digital feito para a cadeira de Segurança de Computadores</p>
        </div>
    
        <h1>Por hoje é só pessoal</h1>
        <img src="{{ url_for('static', filename='finalizando.png') }}" alt="Gato rindo">
    </div>

</body>
</html>
'''

@app.route("/click")
def track_click():
    email_id = request.args.get("id", "desconhecido")
    timestamp = datetime.datetime.now().isoformat()

    # Registra o clique no CSV
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email_id, timestamp])

    print(f"[+] Clique registrado: {email_id} em {timestamp}")

    # Retorna a página de alerta com imagem
    return render_template_string(ALERTA_HTML)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
