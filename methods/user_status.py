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
from api.services import user_status_ssh_service
from methods.manage_users import ManageUsersManager
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime 
import pytz


class UserStatusManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'userstatus': lambda: self.user_status(update, context, db),
            'userstatus_tick': lambda: self.click(update, context, db)
        }

        message_pointer = {
            'userstatus_get_username': lambda: self.user_status_get_username(update, context, db)
        }
        
        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)
            
            if pos in message_pointer :
                await message_pointer[pos]()

    async def user_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id
        query = update.callback_query

        set_position(chat_id, 'userstatus_get_username', db) 

        await query.message.delete()

        inline_options = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')]
                ]
            )

        resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.renew_config_text, reply_markup= inline_options)
        set_msg_id(chat_id, resp_msg.message_id, db)

    async def user_status_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id

        text = update.message.text
        session = get_session(chat_id, db)
        
        resp = user_status_ssh_service(session, text)
        
        if resp.status_code != 200:
            
            if resp.status_code in [404, 409]:
                
                message = loadStrings.text.internal_error

                if resp.json()['detail']['internal_code'] == 2419:
                    message = loadStrings.text.error_not_agent

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

        status_dict = {
            'enable': 'فعال',
            'disable': 'غیرفعال',
            'deleted': 'حذف شده'
        }

        host = resp.json()['services'][0]['detail']['host']
        port = resp.json()['services'][0]['detail']['port']
        username = resp.json()['services'][0]['detail']['username']
        password = resp.json()['services'][0]['detail']['password']
        created = resp.json()['services'][0]['detail']['created']
        expire = resp.json()['services'][0]['detail']['expire']
        status = status_dict[resp.json()['services'][0]['detail']['status']]

        if '+' in created:
            created = created[:-6]

        if '+' in expire:
            expire = expire[:-6]

        format_string = "%Y-%m-%dT%H:%M:%S"  # Replace with the format of your string
        created_timestamp = datetime.strptime(created, format_string).timestamp()
        expire_timestamp = datetime.strptime(expire, format_string).timestamp()

        created = JalaliDateTime.fromtimestamp(created_timestamp, pytz.timezone("Asia/Tehran")).strftime('%Y-%m-%d %H:%M')
        expire = JalaliDateTime.fromtimestamp(expire_timestamp, pytz.timezone("Asia/Tehran")).strftime('%Y-%m-%d %H:%M')

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.tick_for_understrike, callback_data= 'userstatus_tick')
            ]
        ])

        config_text = loadStrings.text.user_status_text.format(host, port, username, password, created, expire, status)
        await context.bot.send_message(chat_id= chat_id, text= config_text, parse_mode='markdown', reply_markup= inline_options)
        set_position(chat_id, 'manageusers', db)
    
        await ManageUsersManager().manager(update, context, edit= False)
    
    async def click(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        query = update.callback_query
        await query.message.delete()
