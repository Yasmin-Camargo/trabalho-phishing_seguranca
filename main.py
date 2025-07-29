from email_server.server import send_email

if __name__ == "__main__":
    plain_text = '''Olá, BIANCA BEPPLER DULLIUS
        Escrevo com urgência sobre sua situação na disciplina de Algoritmos e Programação (22000294).
        
        Ao finalizar o lançamento das notas para o sistema Cobalto, identifiquei uma inconsistência nos seus envios de trabalhos. A sua frequência está em 76%, muito próxima do limite, e a média atual está em 6,8, o que te levaria para o exame final.
        
        O prazo final para digitação das notas é 02 de Setembro, e preciso resolver isso hoje para não te prejudicar. É possível que tenha ocorrido um erro no sistema de upload.
        
        Por favor, acesse o portal de revisão de notas através do link abaixo para verificar os envios que estão pendentes e confirmar sua nota semestral. Você tem até o final do dia para fazer a validação.
        
        Link para revisão: https://cobalto.ufpel.edu.br-portal-academico.net/validar-notas/22000294
        
        A falta de ação resultará na manutenção da nota atual e na necessidade de realizar o exame.
        Atenciosamente,

        Prof. Guilherme Tomaschewski Netto 
        Disciplina de Algoritmos e Programação
        Centro de Desenvolvimento Tecnológico (CDTec)
        Universidade Federal de Pelotas'''

    send_email(plain_text=plain_text, subject="Urgente: Revisão de Notas")
