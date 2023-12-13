import re
import requests

def verify_email_is_valid(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if not (re.search(regex,email)):  
        raise Exception('Email not valid')

    """ endpoint = 'https://www.verifyemailaddress.org/email-validation/result/'
    data = {
        'email': email
    }

    response = requests.post(endpoint, data)
    """

    return True