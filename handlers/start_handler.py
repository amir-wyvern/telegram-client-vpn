
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from lang import loadStrings
from utils.auth import auth
from utils.db_cache import db_cache
from cache.cache_session import set_position
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from methods.menu import MenuManager

@db_cache
@auth
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, db):

    chat_id = update.effective_chat.id 
    set_position(chat_id, 'mainmenu_manager', db)
    await MenuManager().manager(update, context)
    # options = ReplyKeyboardMarkup([
    #     [
    #         KeyboardButton(loadStrings.button.buy_vpn)
    #     ],
    #     [
    #         KeyboardButton(loadStrings.button.increase_balance),
    #         KeyboardButton(loadStrings.button.profile)
    #     ],
    #     [
    #         KeyboardButton(loadStrings.button.support),
    #         KeyboardButton(loadStrings.button.help)
    #     ]
    #     ], resize_keyboard=True) 
    
    
            
    # options = InlineKeyboardMarkup([[InlineKeyboardButton('ddd', callback_data='service_ssh_{0}'.format(2))]])
    
    # await context.bot.send_message(chat_id= tel_id, text= loadStrings.text.start_message, reply_markup=options)


