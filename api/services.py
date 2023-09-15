import requests
from api.config import URL

def _header(session): 

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {session}'
    }

    return headers


def buy_ssh_service(session):

    # plan_id = 1 >> limit : 2 , price 1, duration 30
    data = {
        'plan_id': 1 
    }
    
    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/new', json= data, headers= _header(session))
        if resp.status_code == 200:
            break

    return resp


def buy_test_ssh_service(session):

    # plan_id = 1 >> limit : 2 , price 1, duration 30
    data = {
        'plan_id': 1 
    }
    
    for _ in range(2):
        resp = requests.post(URL + 'agent/ssh/test', json= data, headers= _header(session))
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
        resp = requests.get(URL + 'service/search', params= params, headers= _header(session))
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
        resp = requests.put(URL + 'agent/ssh/expire', json= data, headers= _header(session))
        if resp.status_code == 200:
            break
        
    return resp

