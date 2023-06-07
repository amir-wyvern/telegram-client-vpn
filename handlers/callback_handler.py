from telegram.ext import ContextTypes
from telegram import Update
import requests
from utils.auth import auth
from lang import loadStrings
from utils.db_cache import db_cache
from methods.new_config import NewConfigManager
from methods.menu import MenuManager

newConfigManager = NewConfigManager()
mainmenu = MenuManager()

@db_cache
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    
    query = update.callback_query
    
    # Acknowledge the button click and send a response
    await query.answer()

    callback_poitner = {
        'newconfig' : lambda : newConfigManager.manager(update, context),
        'mainmenu' : lambda : mainmenu.manager(update, context)
    }

    if query.data.split('_')[0] in callback_poitner:
        await callback_poitner[query.data.split('_')[0]]()
    # query = update.callback_query
    # tel_id = query.message.chat.id

    # await query.answer()

    # callback_pointer = {
    #     'service' : lambda : buy_service(update, context)
    # }

    # key = query.data.split('_')[0]

    # if key in callback_pointer:
    #     await callback_pointer[key]()
