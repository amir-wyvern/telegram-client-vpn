
from telegram import Update
from telegram.ext import ContextTypes
from utils.auth import auth
from utils.db_cache import db_cache
from cache.cache_session import get_session, del_session
from api.profile import get_profile
from utils.msg_delete import msg_delete_all
from lang import loadStrings

@db_cache
@auth
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE, db):

    chat_id = update.effective_chat.id 


    session = get_session(chat_id, db)
    resp = get_profile(session)

    if resp.status_code != 200 :

        username= "***"

    else:

        data = resp.json()
        username = data['username']

    del_session(chat_id, db)
    await msg_delete_all(chat_id, db)

    await  context.bot.send_message(chat_id= chat_id, text= loadStrings.text.logout.format(username), parse_mode='markdown')
