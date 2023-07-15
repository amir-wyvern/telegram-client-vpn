from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    set_position,
    get_position,
    get_session,
    set_msg_id
)
from utils.db_cache import db_cache
from api.services import renew_ssh_service
from methods.manage_users import ManageUsersManager

class RenewConfigManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'renewconfig': lambda: self.renew_config(update, context, db),
            'renewconfig_tick': lambda: self.click(update, context, db)
        }

        message_pointer = {
            'renewconfig_get_username': lambda: self.renew_config_get_username(update, context, db)
        }
        
        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)
            
            if pos in message_pointer :
                await message_pointer[pos]()

    async def renew_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id
        query = update.callback_query

        set_position(chat_id, 'renewconfig_get_username', db) 

        await query.message.delete()

        inline_options = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')]
                ]
            )

        resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.renew_config_text, reply_markup= inline_options)
        set_msg_id(chat_id, resp_msg.message_id, db)

    async def renew_config_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id

        text = update.message.text
        session = get_session(chat_id, db)
        
        resp = renew_ssh_service(session, text)

        if resp.status_code != 200:
            
            if resp.status_code in [404, 409, 400]:
                
                message = loadStrings.text.internal_error

                if resp.json()['detail']['internal_code'] == 2433:
                    message = loadStrings.text.error_username_not_have_service

                if resp.json()['detail']['internal_code'] == 2437:
                    message = loadStrings.text.error_service_deleted

                if resp.json()['detail']['internal_code'] == 2419:
                    message = loadStrings.text.error_not_agent

                if resp.json()['detail']['internal_code'] == 2435:
                    message = loadStrings.text.error_not_exist_any_interface

                if resp.json()['detail']['internal_code'] == 2436:
                    message = loadStrings.text.error_not_exist_any_interface

                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')
                    ]
                ])

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)
                return

            else:
        
                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')
                    ]
                ])

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)
                return

        username = resp.json()['username']
        password = resp.json()['password']
        host = resp.json()['host']
        port = resp.json()['port']

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.tick_for_understrike, callback_data= 'renewconfig_tick'),
            ]
        ])
        config_text = loadStrings.text.renew_config_resp.format(host, port, username, password)
        await context.bot.send_message(chat_id= chat_id, text= config_text, parse_mode='markdown', reply_markup=inline_options)
        
        set_position(chat_id, 'manageusers', db)
        
        await ManageUsersManager().manager(update, context, edit= False)

    async def click(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
           send request to server for get new config
        """
        query = update.callback_query

        new_text = []
        for line in query.message.text.split('\n'):
            main_line, strike_line = line.split(' ')
            new_text.append(f'{main_line} <s>{strike_line}</s>')

        join_text=  '\n'.join(new_text).strip()
        await query.edit_message_text(text= join_text, parse_mode='html')
