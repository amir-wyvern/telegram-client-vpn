from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    get_session
)
from utils.db_cache import db_cache
from api.profile import get_profile

class FinancialManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            manager requests this methods 
        """
        query = update.callback_query
    
        self.pointer = {
            'financial': lambda : self.financial(update, context, db),
            'financial_rial_payment': lambda : self.rial_payment(update, context, db),
            'financial_crypto_payment': lambda : self.crypto_payment(update, context, db)
        }
    
        if query.data in self.pointer:
            await self.pointer[query.data]()

    async def financial(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        
        await query.answer()

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.rial_payment, callback_data= 'financial_rial_payment')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.crypto_payment, callback_data= 'financial_crypto_payment')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])
        
        session = get_session(chat_id, db)

        resp = get_profile(session= session)

        if resp.status_code != 200 :
            balance = '***'
        else:

            data = resp.json()
            balance= round(float(data['balance']), 2)

        text= loadStrings.text.financial_detail.format(balance)
        await query.edit_message_text(text= text, reply_markup= inline_options)

    async def rial_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        await query.answer(loadStrings.text.coming_soon)

    async def crypto_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        await query.answer(loadStrings.text.coming_soon)
