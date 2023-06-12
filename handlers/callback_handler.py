from telegram.ext import ContextTypes
from telegram import Update
import requests
from utils.auth import auth
from lang import loadStrings
from utils.db_cache import db_cache
from methods.new_config import NewConfigManager
from methods.menu import MenuManager
from methods.manage_users import ManageUsersManager
from methods.update_expire import UpdateExpireConfigManager
from methods.renew_config import RenewConfigManager


newConfigManager = NewConfigManager()
mainmenu = MenuManager()
manageUsers = ManageUsersManager()
updateExpire = UpdateExpireConfigManager()
renewConfig = RenewConfigManager()

@db_cache
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    
    query = update.callback_query
    
    # Acknowledge the button click and send a response

    callback_poitner = {
        'newconfig' : lambda : newConfigManager.manager(update, context),
        'mainmenu' : lambda : mainmenu.manager(update, context, edit=True),
        'manageusers': lambda: manageUsers.manager(update, context, edit=True),
        'updateexpire': lambda: updateExpire.manager(update, context, edit=True),
        'renewconfig': lambda: renewConfig.manager(update, context, edit=True)
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
