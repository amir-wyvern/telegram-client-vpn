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

    for _ in range(2):
        resp = requests.get(URL + 'interface/ssh/fetch', params= _params, headers= _header(session))
        if resp.status_code == 200:
            break
    
    return resp

def buy_ssh_service(session):

    resp_interface = get_best_interface(session)

    if resp_interface.status_code != 200:
        return resp_interface
    
    data = {
        'interface_id': resp_interface.json()[0]['interface_id']
    }
    
    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/new', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def renew_ssh_service(session, username):

    data = {
        'username': username
    }

    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/renew', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def block_user_ssh_service(session, username):

    data = {
        'username': username
    }
    
    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/block', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def delete_user_ssh_service(session, username):

    data = {
        'username': username
    }
    
    for _ in range(2):
        resp = requests.delete(URL + 'agent/ssh/delete', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def unblock_user_ssh_service(session, username):

    data = {
        'username': username
    }
    
    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/unblock', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def user_status_ssh_service(session, username):

    params = {
        'username': username
    }
    
    for _ in range(2):
        resp = requests.get(URL + 'user/services', params= params, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp

def update_expire_ssh_service(session, username, expire):

    data = {
        'username': username, 
        'new_expire': expire,
        'unblock': True
    }

    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/expire', json= data, headers= _header(session))
        if resp.status_code == 200:
            break
        
    return resp

