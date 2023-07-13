from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    set_position,
    get_position,
    delete_cache,
    set_cache,
    get_cache,
    set_session,
    set_msg_id
)
from utils.db_cache import db_cache
from utils.msg_delete import msg_delete_all
from api.auth import login
from methods.menu import MenuManager


class LoginManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=False):
        """
            manager requests this methods 
        """
        chat_id = update.effective_chat.id
        
        query = update.callback_query

        self.callback_pointer = {
            'login_edit_username': lambda : self.login_username(update, context, db, edit= edit),
            'login_edit_password': lambda : self.login_password(update, context, db, edit= edit)
        }


        self.message_pointer = {
            'login_manager': lambda: self.login_username(update, context, db),
            'login_get_username': lambda: self.login_get_username(update, context, db),
            'login_password': lambda: self.login_password(update, context, db),
            'login_get_password': lambda: self.login_get_password(update, context, db),
            'login_api': lambda: self.login_api(update, context, db)
        }
        
        if edit :

            if query.data in self.callback_pointer: 
                await self.callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)
            
            if pos in self.message_pointer :
                await self.message_pointer[pos]()


    async def login_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            send message for get username
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_get_username', db)

        if edit:
            query = update.callback_query
            await query.edit_message_text(text= loadStrings.text.login_username)
        
        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_username)
            set_msg_id(chat_id, resp_msg.message_id, db)

    async def login_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            get username
        """
        chat_id = update.effective_chat.id
        cache = { 'username':  update.message.text}

        set_cache(chat_id, cache, db)

        await self.login_password(update, context, db)

    async def login_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit= False):
        """
            send message for get password
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_get_password', db)

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.login_edit_username, callback_data= 'login_edit_username'),
            ]
        ])
        
        if edit:
            
            query = update.callback_query
            await query.edit_message_text(text= loadStrings.text.login_password, reply_markup= inline_options)

        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_password, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)

    async def login_get_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            get password
        """

        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, db)
        cache['password'] = update.message.text

        set_cache(chat_id, cache, db)

        set_position(chat_id, 'None', db)

        await self.login_api(update, context, db)

    async def login_api(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            send request to api and get the session
        """
        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, db)

        user_role = 'agent'
        if chat_id == 499985806:
            user_role = 'admin' 

        resp = login(cache['username'], cache['password'], user_role)

        if resp.status_code == 1401:
            options = InlineKeyboardMarkup([[
                InlineKeyboardButton(loadStrings.button.edit_password, callback_data='login_edit_password')
                ]])

            resp_msg = await  context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_failed, reply_markup=options)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return 

        if resp.status_code != 200:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return

        delete_cache(chat_id, db)
        await msg_delete_all(chat_id, db)
        
        set_session(chat_id, resp.json()['access_token'], db)

        await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.inital_msg)
        # link to main menu

        await MenuManager().manager(update, context)

