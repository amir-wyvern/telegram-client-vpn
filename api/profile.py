import requests
from api.config import URL

def _header(session): 

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {session}'
    }

    return headers

def get_profile(session):

    for _ in range(2):
        resp = requests.get(URL + 'agent/info', headers= _header(session))
        if resp.status_code == 200:
            break
        
    return resp



