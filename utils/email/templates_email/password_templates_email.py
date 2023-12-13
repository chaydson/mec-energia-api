from mec_energia import settings

MEC_ENERGIA_URL = settings.MEC_ENERGIA_URL

def template_email_first_access(user_name, link_reset_password_page):
    title = 'Bem Vindo ao Mec Energia'

    message = f'''        
        <h3>Olá {user_name},</h3>

        <p>Bem vindo ao sistema <a href="{MEC_ENERGIA_URL}">MEC Energia</a>.<br>
        Para criar sua senha, clique no link abaixo:</p>

        <p>{link_reset_password_page}</p>

        <p>Se você não solicitou a criação dessa conta, ignore esta mensagem.</p>

        <p>Atenciosamente,<br>
        Equipe MEC Energia.</p>
    '''

    return (title, message)

def template_email_recovery_password(user_name, link_reset_password_page):
    title = 'Recuperação de senha Mec Energia'

    message = f'''
        <h3>Olá {user_name},</h3>

        <p>Foi solicitado a recuperação da sua senha de acesso ao sistema <a href="{MEC_ENERGIA_URL}">MEC Energia</a>.<br>
        Para criar sua nova senha, clique no link abaixo:</p>

        <p>{link_reset_password_page}</p>

        <p>Se você não solicitou a recuperação da senha, ignore esta mensagem.</p>
        
        <p>Atenciosamente,<br>
        Equipe MEC Energia.</p>
    '''

    return (title, message)