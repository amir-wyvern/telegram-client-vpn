from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    set_position,
    get_position,
    delete_cache,
    set_cache,
    get_cache,
    set_session
)
from utils.db_cache import db_cache
from utils.exception import HTTPException

class MenuManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            manager requests this methods 
        """

        chat_id = update.effective_chat.id

        position = get_position(chat_id, db)

        message_pointer = {
            'mainmenu': lambda: self.mainmenu(update, context, db, edit)
        }

        callback_pointer = {
            'mainmenu': lambda: self.mainmenu(update, context, db, edit)
        }

        if edit: 
            
            query = update.callback_query

            if query.data.split('_')[0] in  callback_pointer:
                await callback_pointer[query.data.split('_')[0]]()

        else:
            if position in message_pointer:
                await message_pointer[position]()
        
        # if position not in self.ls_links:
        #     raise HTTPException(status_code=1002, detail=f'THis position not exist in the manager list [{self.__class__}]')

    async def mainmenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            show main menu
        """
        chat_id = update.effective_chat.id
        delete_cache(chat_id, db)

        inline_options = InlineKeyboardMarkup([
            [InlineKeyboardButton(loadStrings.callback_text.new_config, callback_data= 'newconfig')],
            [InlineKeyboardButton(loadStrings.callback_text.manage_users, callback_data= 'manageusers')],
            [   
                InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                InlineKeyboardButton(loadStrings.callback_text.financial, callback_data= 'financial')
            ]
        ])

        if edit: 
            await update.callback_query.edit_message_text( loadStrings.text.menu, reply_markup= inline_options)
        
        else:
            await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.menu, reply_markup= inline_options)
