
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
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
    get_session
)
from utils.db_cache import db_cache
from api.services import update_expire_ssh_service
from datetime import datetime, timedelta
from persiantools.jdatetime import JalaliDateTime
from methods.manage_users import ManageUsersManager
import pytz


class UpdateExpireConfigManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=False):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'updateexpire': lambda : self.update_expire(update, context, db),
            'updateexpire_decrease_expire_day_1': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_increase_expire_day_1': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_decrease_expire_day_10': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_increase_expire_day_10': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_decrease_expire_day_30': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_increase_expire_day_30': lambda: self.update_expire_get_expire_date(update, context, db),
            'updateexpire_expire_submit': lambda: self.update_expire_submit(update, context, db)
        }

        message_pointer = {
            'updateexpire_get_username': lambda: self.update_expire_get_username(update, context, db)
        }
        if edit :
            print(query.data)

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)

            if pos in message_pointer :
                await message_pointer[pos]()


    async def update_expire(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id
        query = update.callback_query

        set_position(chat_id, 'updateexpire_get_username', db) 

        await query.message.delete()

        inline_options = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')]
                ]
            )
        
        await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.update_expire_get_username_text, reply_markup= inline_options)

    async def update_expire_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id

        text = update.message.text

        cache = {
            'username': text
        }
        set_cache(chat_id, cache, db)
        await self.update_expire_set_date(update, context, db)

    async def update_expire_set_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):

        chat_id = update.effective_chat.id

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_1, callback_data= 'updateexpire_decrease_expire_day_1'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_1, callback_data= 'updateexpire_increase_expire_day_1')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_10, callback_data= 'updateexpire_decrease_expire_day_10'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_10, callback_data= 'updateexpire_increase_expire_day_10')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_30, callback_data= 'updateexpire_decrease_expire_day_30'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_30, callback_data= 'updateexpire_increase_expire_day_30')

            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'updateexpire_submit'),
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'updateexpire')
            ]
        ])

        date_day = JalaliDateTime.now(pytz.utc)

        cache = get_cache(chat_id, db)
        if 'number_day' in cache:
            date_day =  date_day + timedelta(days=cache['number_day'])

        text_day = loadStrings.text.expire_day_text.format(date_day.strftime("%Y/%m/%d"))
        await context.bot.send_message(chat_id= chat_id, text= text_day, reply_markup= inline_options)
        

    async def update_expire_get_expire_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):

        chat_id = update.effective_chat.id
        query = update.callback_query

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_1, callback_data= 'updateexpire_decrease_expire_day_1'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_1, callback_data= 'updateexpire_increase_expire_day_1')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_10, callback_data= 'updateexpire_decrease_expire_day_10'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_10, callback_data= 'updateexpire_increase_expire_day_10')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.decrease_day_30, callback_data= 'updateexpire_decrease_expire_day_30'),
                InlineKeyboardButton(loadStrings.callback_text.increase_day_30, callback_data= 'updateexpire_increase_expire_day_30')

            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'updateexpire_expire_submit'),
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'updateexpire')
            ]
        ])

        day_dict = {
            'updateexpire_decrease_expire_day_1': -1,
            'updateexpire_increase_expire_day_1': 1,
            'updateexpire_decrease_expire_day_10': -10,
            'updateexpire_increase_expire_day_10': 10,
            'updateexpire_decrease_expire_day_30': -30,
            'updateexpire_increase_expire_day_30': 30
        }
        date_day = JalaliDateTime.now(pytz.utc)

        cache = get_cache(chat_id, db)

        number_day = day_dict[query.data]

        date_day = date_day + timedelta(days= number_day)
        
        if 'number_day' in cache:
            number_day += cache['number_day']
            date_day =  date_day + timedelta(days=cache['number_day'])

        cache['number_day'] = number_day
        set_cache(chat_id, cache, db)

        text_day = loadStrings.text.expire_day_text.format(date_day.strftime("%Y/%m/%d"))

        await update.callback_query.edit_message_text( text_day, reply_markup= inline_options)

    async def update_expire_submit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):

        chat_id = update.effective_chat.id
        query = update.callback_query

        session = get_session(chat_id, db)
        
        cache = get_cache(chat_id, db)
        
        if 'number_day' not in cache:
            await query.answer(loadStrings.text.empty_day_field)
            return

        new_expire = datetime.now() + timedelta(days= cache['number_day'])
        username = cache['username']
        resp = update_expire_ssh_service(session, username, new_expire.strftime('%Y-%m-%dT%H:%M:%S'))

        if resp.status_code != 200:
            
            if resp.status_code in [404, 409]:
                    
                if resp.json()['detail']['internal_code'] == 2433:
                    message = loadStrings.text.error_username_not_have_service

                if resp.json()['detail']['internal_code'] == 2437:
                    message = loadStrings.text.error_service_deleted

                if resp.json()['detail']['internal_code'] == 2419:
                    message = loadStrings.text.error_not_agent
                
                if resp.json()['detail']['internal_code'] == 1412:
                    message = loadStrings.text.insufficient_balance

                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'updateexpire')
                    ]
                ])

                await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
                return

            else:
                
                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'updateexpire')
                    ]
                ])

                await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error, reply_markup= inline_options)
                return
        
        set_position(chat_id, 'manageusers', db)
        delete_cache(chat_id, db)
        new_expire_jalali = (JalaliDateTime.now() + timedelta(days= cache['number_day']) ).strftime("%Y/%m/%d")

        message = loadStrings.text.update_expire_success.format(username, new_expire_jalali) 
        await context.bot.send_message(chat_id= chat_id, text= message, parse_mode='markdown') 
        await ManageUsersManager().manager(update, context, edit= False) 
