import json
import re
import requests
​
​
def get_csrf_token(session):

    login_response = session.get('https://login.uber.com/login')

    csrf_token_pattern = '<input type="hidden" name="_csrf_token" value="([a-zA-Z0-9\_\-\=]+)">'

    csrf_token = re.search(csrf_token_pattern, login_response.text).group(1)

    return csrf_token

def login(session):
    csrf_token = get_csrf_token(session)

    data = {
        'email': 'julio_jr3@hotmail.com',
        'password': 'juliojr77julio7',
        '_csrf_token': csrf_token,
        'access_token': ''
    }

    login_response = session.post('https://login.uber.com/login', data)


def get_statement(session, id):

    url = 'https://partners.uber.com/p3/money/statements/view/{}'.format(id)

    statement_response = session.get(url)

    data = json.loads(statement_response.text)

    return data
​
​
session = requests.Session()
​
login(session)
​
data = get_statement(session, 'c3d4b2e0-935b-1a93-eb05-8a59f2bc5ac1')
​
print(data['body']) # ['driver']['trips']
