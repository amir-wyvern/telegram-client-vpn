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

    resp = db.hset(f'tel:agent:{chat_id}', mapping= data)
    return resp

def set_session(chat_id, session, db: redis.Redis):

    resp = db.hset(f'tel:agent:{chat_id}', 'session', session)
    return resp

def get_session(chat_id, db: redis.Redis):

    session = db.hget(f'tel:agent:{chat_id}', 'session') 
    if session :

        return session

    return None

def set_position(chat_id, pos, db:redis.Redis):

    resp = db.hset(f'tel:agent:{chat_id}', 'pos', pos)
    return resp

def get_position(chat_id, db:redis.Redis):

    pos =db.hget(f'tel:agent:{chat_id}', 'pos')
    return pos

def set_cache(chat_id, data, db:redis.Redis):

    resp = db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps(data))
    return resp

def delete_cache(chat_id, db:redis.Redis):

    db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps({}))
    return True

def get_cache(chat_id, db:redis.Redis):

    data = db.hget(f'tel:agent:{chat_id}', 'cache')
    return json.loads(data)

def set_msg_id(chat_id, msg_id, db: redis.Redis):

    resp = db.rpush(f'tel:agent:msg_id:{chat_id}', msg_id)
    return resp

def get_msg_id(chat_id, db: redis.Redis):

    data = db.lrange(f'tel:agent:msg_id:{chat_id}', start=0 ,end=-1)
    return data

def remove_msg_id(chat_id, msg_id, db: redis.Redis):

    resp = db.lrem(f'tel:agent:msg_id:{chat_id}', count=1, value= msg_id)
    return resp