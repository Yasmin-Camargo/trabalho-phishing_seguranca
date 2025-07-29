# red_team/templates.py

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

