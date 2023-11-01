from cache.cache_session import get_session, set_position
from methods.login import LoginManager

def auth(func):

    async def wrapper(*args, **kwargs):

        if kwargs.get('db', None) is None:
            raise 'db decorator is not used'


        if hasattr(args[1], '_chat_id'):
            chat_id = args[1]._chat_id
            _args = args
        else:
            chat_id = args[1].effective_chat.id
            _args = args[1:]

        session = get_session(chat_id, kwargs['db'])
        if session is None:

            set_position(chat_id, 'login_manager', kwargs['db'])

            await LoginManager().manager(*_args, db=kwargs['db'])
            return


        result = await func(*args, **kwargs)
        return result

    return wrapper
