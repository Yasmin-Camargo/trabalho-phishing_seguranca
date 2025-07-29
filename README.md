# trabalho-phishing_seguranca
Trabalho desenvolvido para a disciplina de Segurança de computadores que tem o objetivo de simular campanhas de phishing por meio de e-mails gerados.


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
