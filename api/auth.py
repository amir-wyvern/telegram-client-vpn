import requests
from api.config import URL
from utils.exception import HTTPException

def login(username, password):

    headers = {
       'accept': 'application/json',
       'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
      'grant type' :'',
      'username': username,
      'password': password,
      'scope': 'admin',
    #   'scope': 'agent',
      'client_id': '',
      'client_secret': ''
      }
    resp = requests.post(URL + 'auth/login', data= data, headers= headers) 
    
    if resp.status_code == 401:
        return HTTPException(status_code= 1401, detail='Incorrect username or password')
    
    if resp.status_code != 200:
        raise HTTPException(status_code= resp.status_code, detail=resp.content)
    
    return resp
