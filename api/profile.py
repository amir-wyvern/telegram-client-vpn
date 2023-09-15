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

def claim_profit_via_wallet(session, value):

    data = {
        'value': value,
        'method': 'wallet'
    }
    for _ in range(2):
        resp = requests.post(URL + 'agent/subset/profit', json= data, headers= _header(session))
        if resp.status_code == 200:
            break
        
    return resp


def set_chat_id(session, chat_id):
    data = {
        'new_chat_id': chat_id
    }
    resp = None
    for _ in range(2):
        try:
            resp = requests.put(URL + 'agent/chat_id', json= data, headers= _header(session))
            if resp.status_code == 200:
                break
            
        except:
            pass

    return resp 

