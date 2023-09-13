from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    get_position,
    delete_cache,
    set_msg_id,
    set_position,
    get_session
)
from utils.db_cache import db_cache
from api.profile import get_profile

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

        set_position(chat_id, 'mainmenu', db)

        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.new_config, callback_data= 'newconfig'),
                InlineKeyboardButton(loadStrings.callback_text.test_config_key, callback_data= 'testconfig')
            ],
            [InlineKeyboardButton(loadStrings.callback_text.manage_users, callback_data= 'manageusers')],
            [InlineKeyboardButton(loadStrings.callback_text.profile_key, callback_data= 'profile')],
            [   
                InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                InlineKeyboardButton(loadStrings.callback_text.financial, callback_data= 'financial')
            ]
        ])

        session = get_session(chat_id, db)
        resp = get_profile(session)

        if resp.status_code != 200 :
            # inline_options = InlineKeyboardMarkup([
            #     [   
            #         InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support)
            #     ]
            # ])

            # resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_config, reply_markup= inline_options)
            # set_msg_id(chat_id, resp_msg.message_id, db)

            username= "***"
            balance= "***"
            total_user= "***"
            enable_ssh_services= "***"
            disable_ssh_services= "***"
            deleted_ssh_services= "***"

        else:

            data = resp.json()
            username= data['username']
            balance= data['balance']
            total_user= data['total_user']
            enable_ssh_services= data['enable_ssh_services']
            disable_ssh_services= data['disable_ssh_services']
            deleted_ssh_services= data['deleted_ssh_services']
        
        text = loadStrings.text.menu.format(username, total_user, enable_ssh_services, disable_ssh_services, deleted_ssh_services, balance)
        if edit: 
            resp_msg = await update.callback_query.edit_message_text( text, reply_markup= inline_options)
        
        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= text, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)