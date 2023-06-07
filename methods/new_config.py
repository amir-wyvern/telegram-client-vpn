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

class NewConfigManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, backward= False):
        """
            manager requests this methods 
        """
        query = update.callback_query
        chat_id = query.message.chat_id
    
        self.pointer = {
            'newconfig': lambda : self.newconfig_number(update, context, db),
            'newconfig_increase_number': lambda : self.increase_number_config(update, context, db),
            'newconfig_decrease_number': lambda : self.decrease_number_config(update, context, db),
            'newconfig_sumbit': lambda : self.submit(update, context, db),
        }
    
        if query.data in self.pointer:
            await self.pointer[query.data]()

    async def newconfig_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        
        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.increase_number_config, callback_data= 'newconfig_increase_number'),
                InlineKeyboardButton(loadStrings.callback_text.decrease_number_config, callback_data= 'newconfig_decrease_number')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'newconfig_submit')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])
        
        cache = get_cache(chat_id, db)
        
        number = 0

        if 'number_config' in cache:
            number = cache['number_config']
        
        await query.edit_message_text(text= loadStrings.text.select_number_newconfig.format(number), reply_markup= inline_options)
    

    async def increase_number_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id

        cache = get_cache(chat_id, db)

        number = 0
        if 'number_config' in cache:
            number = cache['number_config']
        
        number += 1
        data = {
            'number_config' : number
        }

        set_cache(chat_id, data, db)

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.increase_number_config, callback_data= 'newconfig_increase_number'),
                InlineKeyboardButton(loadStrings.callback_text.decrease_number_config, callback_data= 'newconfig_decrease_number')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'newconfig_submit')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])

        await query.edit_message_text(text= loadStrings.text.select_number_newconfig.format(number), reply_markup= inline_options)
    
    async def decrease_number_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id

        cache = get_cache(chat_id, db)

        number = 0
        if 'number_config' in cache:
            number = cache['number_config']
        
        if number > 0:
            number -= 1
        
            data = {
                'number_config' : number
            }

            set_cache(chat_id, data, db)

            inline_options = InlineKeyboardMarkup([
                [   
                    InlineKeyboardButton(loadStrings.callback_text.increase_number_config, callback_data= 'newconfig_increase_number'),
                    InlineKeyboardButton(loadStrings.callback_text.decrease_number_config, callback_data= 'newconfig_decrease_number')
                ],
                [
                    InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'newconfig_submit')
                ],
                [
                    InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
                ]
            ])

            await query.edit_message_text(text= loadStrings.text.select_number_newconfig.format(number), reply_markup= inline_options)
        
    async def submit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
           send request to server for get new config
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        print('submit')
        # print(chat_id)    
        # inline_options = InlineKeyboardMarkup([
        #     [   
        #         InlineKeyboardButton(loadStrings.callback_text.increase_number_config, callback= loadStrings.callback_key.increase_number_config),
        #         InlineKeyboardButton(loadStrings.callback_text.decrease_number_config, callback= loadStrings.callback_key.decrease_number_config)
        #     ]
        # ])
        # await query.edit_message_text(text= loadStrings.text.select_number_newconfig, reply_markup= inline_options)
