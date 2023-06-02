from telegram.ext import ContextTypes
from telegram import Update
import requests
from utils.auth import auth



async def buy_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    _, service_type, interface_id = query.data.split('_')

    requests.post()

@auth
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    print('-------------')
    print(context._chat_id)
    # query = update.callback_query
    # tel_id = query.message.chat.id

    # await query.answer()

    # callback_pointer = {
    #     'service' : lambda : buy_service(update, context)
    # }

    # key = query.data.split('_')[0]

    # if key in callback_pointer:
    #     await callback_pointer[key]()
