from flask import Flask, request, redirect
import csv
import datetime
import os

app = Flask(__name__)
LOG_FILE = "cliques.csv"

# Garante que o CSV exista com cabeçalho
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email_id", "timestamp"])

@app.route("/click")
def track_click():
    email_id = request.args.get("id", "desconhecido")
    timestamp = datetime.datetime.now().isoformat()

    # Registra o clique no CSV
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([email_id, timestamp])

    print(f"[+] Clique registrado: {email_id} em {timestamp}")

    # Redireciona para o site real
    return redirect("https://fluffy-gumdrop-ab8e4c.netlify.app/")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
