from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_username)

