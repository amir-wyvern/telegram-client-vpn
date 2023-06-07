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

    def __init__(self) -> None:

        self.ls_links = ['mainmenu_manager', 'mainmenu']

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

    async def mainmenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        chat_id = update.effective_chat.id
        delete_cache(chat_id, db)

        inline_options = InlineKeyboardMarkup([
            [InlineKeyboardButton(loadStrings.callback_text.new_config, callback_data= 'newconfig')],
            [InlineKeyboardButton(loadStrings.callback_text.manage_users, callback_data= 'manage_users')],
            [   
                InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                InlineKeyboardButton(loadStrings.callback_text.financial, callback_data= 'financial')
            ]
        ])

        if getattr(update, 'callback_query') : 
            await update.callback_query.edit_message_text( loadStrings.text.menu, reply_markup= inline_options)
        
        else:
            await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.menu, reply_markup= inline_options)
