from google import genai
from google.genai import types
from pydantic import BaseModel

class PhishingEmail(BaseModel):
    subject: str
    fake_sender_name: str
    email: str

prompt = '''
    Você é um especialista em cibersegurança criando conteúdo para uma simulação de conscientização sobre phishing em um curso de Ciência da Computação da UFPel.

    Crie um e-mail de phishing convincente usando a estrutura abaixo:

    1. **Cenário e Gancho (O Quê?)**  
    Escolha um tema verossímil e relevante para o público-alvo. Exemplos:  
    - Acadêmico: notas, frequência, trabalhos, exames.  
    - Administrativo: matrícula, trancamento, calendário, regras.  
    - Financeiro: bolsas, auxílios, cobranças falsas.  
    - Técnico/TI: alertas de segurança, atualização de conta, cota de e-mail.  
    - Oportunidade/Eventos: convites, palestras, pesquisas, vagas.  

    2. **Gatilho Psicológico (O Porquê?)**  
    Defina a emoção ou viés cognitivo que motiva a ação imediata:  
    - Medo (perda de vaga, conta bloqueada)  
    - Urgência (prazo curto)  
    - Autoridade (mensagem de coordenador/professor/TI)  
    - Ganância/Oportunidade (benefício inesperado)  
    - Confiança (pessoa ou instituição conhecida)  
    - Curiosidade (descobrir algo instigante)  

    3. **Tom de Voz (O Como?)**  
    Ajuste o tom conforme o cenário/gatilho:  
    - Alarmista: "AVISO URGENTE", "AÇÃO NECESSÁRIA"  
    - Formal: "Em conformidade com a portaria..."  
    - Amigável: "Oi pessoal, para ajudar vocês..."  
    - Exclusivo: "Parabéns, você foi selecionado..."  

    4. **Estrutura do E-mail**  
    - **Assunto:** breve, chamativo e coerente com o gatilho.  
    - **Remetente Falso:** plausível mas não real (ex.: `secretaria@uffpel.edu.br` com erro sutil).  
    - **Corpo:**  
        - Saudação personalizada: `Olá, {name},`  
        - Contexto inicial crível  
        - Problema ou oportunidade  
        - Chamada para ação (CTA) com link malicioso: `link.com.br`  
        - Consequência ou reforço da urgência  
    - **Link:** sempre usar `link.com.br` como destino.  

    ---

    ## INFORMAÇÕES GERAIS DO CURSO - CIÊNCIA DA COMPUTAÇÃO UFPel

    **Curso:** Ciência da Computação  
    **Centro:** Centro de Desenvolvimento Tecnológico (CDTec)  

    ### DISCIPLINAS DO 1º SEMESTRE
    - **22000294** - Algoritmos e Programação (Prof. Guilherme Tomaschewski Netto)
    - **22000196** - Introdução à Ciência da Computação (Prof. Weslen Schiavon de Souza)
    - **22000207** - Laboratório de Computação (Prof. Weslen Schiavon de Souza)
    - **22000224** - Lógica para Computação (Prof. Larissa Astrogildo de Freitas)
    - **22000293** - Sistemas Discretos (Prof. Simone Andre da Costa Cavalheiro)

    ### DATAS IMPORTANTES
    - **02 de Setembro:** Data limite para digitação de notas 2025/1
    - **22 de Agosto:** Prazo final para trancamento geral de matrícula
    - **23 de Agosto:** Último dia letivo de 2025/1
    - **25-30 de Agosto:** Período de exames 2025/1
    - **15 de Setembro:** Início do semestre 2025/2

    ### SISTEMA COBALTO
    - Sistema oficial de gestão acadêmica da UFPel
    - Portal para consulta de notas, matrículas e informações acadêmicas
    - URL oficial: cobalto.ufpel.edu.br

    ---

    > Use `\n` para espaçar o corpo do e-mail.  
    > Variáveis: `{name}`, `{email}`

'''

def generate_phishing_email():
    try:
        client = genai.Client()
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PhishingEmail,
            ),
        )
        return response.text
    except Exception as e:
        print(f"API não disponível: {e}")


def get_default_plain_text():
    return (
        "Dear students,\n\n"
        "On Friday, June 27, we will have a meeting at 17:10, room 343.\n"
        "Looking forward to seeing you.\n\n"
        "Prof. Lisane"
    )


def get_cobalto_html_body(plain_text):
    plain_text_html = plain_text.replace('\n', '<br>')
    return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Meeting - UFPel</title>
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
        </html>
    """

