from cache.cache_session import get_session
from cache.database import get_redis_cache


def auth(func):

    async def wrapper(*args, **kwargs):
        
        cache_db = get_redis_cache().__next__()
        session = get_session(args[1]._chat_id, cache_db)
        
        if session is None:


        
        kwargs['session'] = None
        print("Before function execution")
        # get_redis_cache()
        result = await func(*args, **kwargs)
        print("After function execution")
        return result
    
    return wrapper