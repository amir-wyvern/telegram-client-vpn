import requests
from api.config import URL
from utils.exception import HTTPException

def login(username, password, user_role):

    headers = {
       'accept': 'application/json',
       'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
      'grant type' :'',
      'username': username,
      'password': password,
      'scope': user_role,
      'client_id': '',
      'client_secret': ''
    }

    for _ in range(2):
      resp = requests.post(URL + 'auth/login', data= data, headers= headers) 
      if resp.status_code == 200:
            break
      
    if resp.status_code == 401:
        return HTTPException(status_code= 1401, detail='Incorrect username or password')
    
    if resp.status_code != 200:
        raise HTTPException(status_code= resp.status_code, detail=resp.content)
    
    return resp
