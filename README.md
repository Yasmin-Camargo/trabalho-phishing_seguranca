# trabalho-phishing_seguranca
Trabalho desenvolvido para a disciplina de Segurança de Computadores que simula campanhas de phishing através de e-mails gerados automaticamente.


## 📋 Descrição

Este projeto é um simulador educacional que gera automaticamente e-mails de phishing personalizados com base em uma lista de contatos (arquivo `contatos.csv`). O sistema utiliza inteligência artificial para criar conteúdo convincente e realista, permitindo estudar e compreender as técnicas utilizadas em ataques de engenharia social.

**⚠️ IMPORTANTE: Este projeto é exclusivamente para fins de teste e educação em segurança digital. Não deve ser utilizado para atividades maliciosas ou ilegais.**


## Como executar o MailHog com Docker

1. **Instale o Docker**  

2. **Execute o MailHog**  
    No terminal, rode o comando abaixo para iniciar o MailHog em segundo plano:

    ```bash
    docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
    ```

3. **Acesse a interface web**  
    Abra seu navegador e acesse: [http://localhost:8025](http://localhost:8025)

Assim, você poderá visualizar os e-mails enviados durante os testes de phishing.


### Configure a API do Google Gemini

```bash
export GEMINI_API_KEY="sua_chave_aqui"
```

### Execute o simulador
```bash
python3 main.py
```

Exemplo de email enviado:
<img width="1920" height="543" alt="image" src="https://github.com/user-attachments/assets/b55253e9-0a15-42e0-9e33-79c4883a9361" />
<img width="1908" height="923" alt="image" src="https://github.com/user-attachments/assets/3f494e7b-2c59-41d2-a758-7ba3ccf3088b" />
