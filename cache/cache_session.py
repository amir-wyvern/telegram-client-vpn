import redis
import json


def get_user(chat_id, item, db: redis.Redis):

    if item == 'all':
        resp = db.hgetall(f'tel:agent:{chat_id}')
        if resp == {}:
            resp = None
        
        # if resp['cache'] != {}
        return resp
    
    else:
        return db.hget(f'tel:agent:{chat_id}', item)
    
def set_new_user(chat_id, db: redis.Redis, **kwargs)-> dict:

    data = {
        'pos':'menu',
        'cache': json.dumps({}),
        'session': ''
    }
    data.update(kwargs)

    db.hset(f'tel:agent:{chat_id}', mapping= data)
    return data

def set_session(chat_id, session, db: redis.Redis):

    resp = db.hset(f'tel:agent:{chat_id}', 'session', session)
    return resp

def get_session(chat_id, db: redis.Redis):

    session = db.hget(f'tel:agent:{chat_id}', 'session') 
    if session :

        return session

    return None

def set_position(chat_id, pos, db:redis.Redis):

    db.hset(f'tel:agent:{chat_id}', 'pos', pos)
    return pos

def get_position(chat_id, db:redis.Redis):

    pos =db.hget(f'tel:agent:{chat_id}', 'pos')
    return pos

def set_cache(chat_id, data, db:redis.Redis):

    x = db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps(data))
    return data

def delete_cache(chat_id, db:redis.Redis):

    db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps({}))
    return True

def get_cache(chat_id, db:redis.Redis):

    data = db.hget(f'tel:agent:{chat_id}', 'cache')
    return json.loads(data)