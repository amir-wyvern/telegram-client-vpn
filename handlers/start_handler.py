
from telegram import Update
from telegram.ext import ContextTypes
from utils.auth import auth
from utils.db_cache import db_cache
from cache.cache_session import set_position, set_msg_id
from methods.menu import MenuManager
from utils.msg_delete import msg_delete_all

@db_cache
@auth
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, db):

    chat_id = update.effective_chat.id 

    set_position(chat_id, 'mainmenu', db)
    await msg_delete_all(chat_id, db)

    set_msg_id(chat_id, update.message.message_id, db)
    await MenuManager().manager(update, context)

