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
    set_msg_id,
    get_session,
    set_position
)
from utils.db_cache import db_cache
from api.profile import get_profile
from utils.auth import auth

class ManageUsersManager:


    @db_cache
    @auth
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'manageusers': lambda : self.manageusers(update, context, db, edit=edit),
        }

        message_pointer = {
            'manageusers': lambda : self.manageusers(update, context, db, edit=edit),
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
        set_position(chat_id, 'manageusers', db)


        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.renew_user, callback_data= 'renewconfig'),
                InlineKeyboardButton(loadStrings.callback_text.sharge_config, callback_data= 'updateexpire')
            ],
            [   
                InlineKeyboardButton(loadStrings.callback_text.block_user, callback_data= 'blockuser'),
                InlineKeyboardButton(loadStrings.callback_text.delete_user, callback_data= 'deleteuser'),
                InlineKeyboardButton(loadStrings.callback_text.unblock_user, callback_data= 'unblockuser')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.status_user, callback_data= 'userstatus')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.help, callback_data= 'help'),
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
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
            total_user= "***"
            enable_ssh_services= "***"
            disable_ssh_services= "***"
            expired_ssh_services= "***"
            deleted_ssh_services= "***"
            test_ssh_services= "***"

        else:

            data = resp.json()
            username= data['username']
            total_user= data['total_user']
            enable_ssh_services= data['enable_ssh_services']
            disable_ssh_services= data['disable_ssh_services']
            expired_ssh_services= data['expired_ssh_services']
            deleted_ssh_services= data['deleted_ssh_services']
            test_ssh_services= data['test_ssh_services']
        
        text = loadStrings.text.usersmanager_menu.format(username, total_user, test_ssh_services, enable_ssh_services, disable_ssh_services, expired_ssh_services, deleted_ssh_services)

        if edit:
            await update.callback_query.edit_message_text( text, reply_markup= inline_options)

        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= text, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)
