import requests
from api.config import URL

def _header(session): 

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {session}'
    }

    return headers

def get_best_interface(session):

    _params = {'mode': 'best'}
    resp = requests.get(URL + 'interface/ssh/fetch', params= _params, headers= _header(session))
    return resp

def buy_ssh_service(session):

    resp_interface = get_best_interface(session)

    if resp_interface.status_code != 200:
        return resp_interface
    
    data = {
        'interface_id': resp_interface.json()[0]['interface_id']
    }
    
    resp = requests.post(URL + 'agent/ssh/new', json= data, headers= _header(session))

    return resp

def renew_ssh_service(session, username):

    data = {
        'username': username
    }
    
    resp = requests.post(URL + 'agent/ssh/renew', json= data, headers= _header(session))

    return resp

def update_expire_ssh_service(session, username, expire):

    data = {
        'username': username, 
        'new_expire': expire
    }
    
    resp = requests.post(URL + 'agent/ssh/expire', json= data, headers= _header(session))

    return resp