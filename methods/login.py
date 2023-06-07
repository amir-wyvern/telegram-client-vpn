from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
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
from api.auth import login

class LoginManager:

    def __init__(self) -> None:

        self.ls_links = ['login_manager','login_username', 'login_get_username', 'login_password', 'login_get_password', 'login_api']

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, backward= False):
        """
            manager requests this methods 
        """
        chat_id = update.effective_chat.id
        
        position = get_position(chat_id, db) 
        if position not in self.ls_links:
            raise HTTPException(status_code=1002, detail=f'THis position not exist in the manager list [{self.__class__}]')

        index_pos = self.ls_links.index(position)
        
        if backward:
            new_position = self.ls_links[index_pos-1] 
        
        else:
            new_position = self.ls_links[index_pos+1] 
        
        await getattr(self, new_position)(update, context, db)


    async def login_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            send message for get username
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_username', db)

        await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_username)

    async def login_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            get username
        """
        chat_id = update.effective_chat.id
        cache = { 'username':  update.message.text}

        set_cache(chat_id, cache, db)

        await self.login_password(update, context, db)

    async def login_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            send message for get password
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_password', db)
        await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_password)

    async def login_get_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            get password
        """

        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, db)
        cache['password'] = update.message.text

        set_cache(chat_id, cache, db)

        await self.login_api(update, context, db)

    async def login_api(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            send request to api and get the session
        """
        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, db)

        resp = login(cache['username'], cache['password'])
        print('resp')
        if resp.status_code == 1401:
            options = InlineKeyboardMarkup([
                InlineKeyboardButton(loadStrings.button.edit_password, 'edit_password')
                ], resize_keyboard=True)
            
            await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_failed, reply_markup=options)

        if resp.status_code != 200:
            await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error)

        set_session(chat_id, resp.json()['access_token'], db)
        set_position(chat_id, 'mainmenu', db)
        delete_cache(chat_id, db)
        await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_success)
        # link to main menu

