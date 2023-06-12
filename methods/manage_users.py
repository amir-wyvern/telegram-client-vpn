from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
) 
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    get_position,
    delete_cache,
)
from utils.db_cache import db_cache

class ManageUsersManager:


    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'manageusers': lambda : self.manageusers(update, context, db, edit=edit),
            'manageusers_renew_user': lambda: self.renew_config(update, context, db),
            'manageusers_renew_config_get_username': lambda: self.renew_config_get_username(update, context, db),
        }

        message_pointer = {
            'manageusers': lambda : self.manageusers(update, context, db, edit=edit),
            'manageusers_get_renew_config': lambda: self.renew_config_get_username(update, context, db)
        }
        
        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)

            if pos in message_pointer :
                await message_pointer[pos]()

    async def manageusers(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            show main menu
        """
        chat_id = update.effective_chat.id

        delete_cache(chat_id, db)

        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.renew_user, callback_data= 'renewconfig'),
                InlineKeyboardButton(loadStrings.callback_text.sharge_config, callback_data= 'updateexpire')
            ],
            [   
                InlineKeyboardButton(loadStrings.callback_text.block_user, callback_data= 'manageusers_block_user'),
                InlineKeyboardButton(loadStrings.callback_text.unblock_user, callback_data= 'manageusers_unblock_user'),
                InlineKeyboardButton(loadStrings.callback_text.status_user, callback_data= 'manageusers_status_user')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.agent_users, callback_data= 'manageusers_agent_users')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.help, callback_data= 'manageusers_help'),
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])

        if edit:
            await update.callback_query.edit_message_text( loadStrings.text.menu, reply_markup= inline_options)

        else:
            await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.menu, reply_markup= inline_options)



