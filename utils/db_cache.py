from cache.cache_session import get_session
from cache.database import get_redis_cache


def db_cache(func):

    async def wrapper(*args, **kwargs):
        
        db_cache = get_redis_cache().__next__()
        kwargs.update({'db': db_cache})
        print('func : ',func)
        result = await func(*args, **kwargs)
        return result
    
    return wrapper