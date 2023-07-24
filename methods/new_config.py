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
    set_cache,
    get_cache,
    get_session,
    set_msg_id
)
from utils.db_cache import db_cache
from api.services import buy_ssh_service
from api.profile import get_profile
from methods.menu import MenuManager


class NewConfigManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, backward= False):
        """
            manager requests this methods 
        """
        query = update.callback_query
    
        self.pointer = {
            'newconfig': lambda : self.newconfig_number(update, context, db),
            'newconfig_increase_number': lambda : self.increase_config_number(update, context, db),
            'newconfig_decrease_number': lambda : self.decrease_config_number(update, context, db),
            'newconfig_submit': lambda : self.submit(update, context, db),
            'newconfig_tick': lambda : self.click(update, context, db),
        }
    
        if query.data in self.pointer:
            await self.pointer[query.data]()

    async def newconfig_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        
        await query.answer()

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.increase_config_number, callback_data= 'newconfig_increase_number'),
                InlineKeyboardButton(loadStrings.callback_text.decrease_config_number, callback_data= 'newconfig_decrease_number')
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

        if 'config_number' in cache:
            number = cache['config_number']
        
        await query.edit_message_text(text= loadStrings.text.select_number_newconfig.format(number), reply_markup= inline_options)
    

    async def increase_config_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id

        cache = get_cache(chat_id, db)

        number = 0
        if 'config_number' in cache:
            number = cache['config_number']
        
        number += 1

        if number > 5 :
            await query.answer(loadStrings.text.max_config)
            return
        
        await query.answer()

        data = {
            'config_number' : number
        }

        set_cache(chat_id, data, db)

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.increase_config_number, callback_data= 'newconfig_increase_number'),
                InlineKeyboardButton(loadStrings.callback_text.decrease_config_number, callback_data= 'newconfig_decrease_number')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.submit, callback_data= 'newconfig_submit')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])

        await query.edit_message_text(text= loadStrings.text.select_number_newconfig.format(number), reply_markup= inline_options)
    
    async def decrease_config_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show main menu
        """
        query = update.callback_query
        chat_id = query.message.chat_id
        await query.answer()

        cache = get_cache(chat_id, db)

        number = 0
        if 'config_number' in cache:
            number = cache['config_number']
        
        if number > 0:
            number -= 1
            
            data = {
                'config_number' : number
            }

            set_cache(chat_id, data, db)

            inline_options = InlineKeyboardMarkup([
                [   
                    InlineKeyboardButton(loadStrings.callback_text.increase_config_number, callback_data= 'newconfig_increase_number'),
                    InlineKeyboardButton(loadStrings.callback_text.decrease_config_number, callback_data= 'newconfig_decrease_number')
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

        cache = get_cache(chat_id, db)

        if 'config_number' not in cache:
            await query.answer(loadStrings.text.zero_number_config)
            return
        
        number = cache['config_number']
        if number == 0:
            await query.answer(loadStrings.text.zero_number_config)
            return
        
        try:
            await query.message.delete()
        
        except:
            inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support)
                    ]
                ])
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_delete_msg, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return 
        
        session = get_session(chat_id, db)
        resp = get_profile(session)
        total_config = '***'
        if resp.status_code == 200 :
            total_config = int(resp.json()['total_user'])

        for count in range(number):
            resp = buy_ssh_service(session)


            if resp.status_code != 200 :

                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'newconfig')
                    ]
                ])

                if resp.status_code in [404, 409]:
                
                    message = loadStrings.text.internal_error
                
                    if resp.json()['detail']['internal_code'] == 1412:
                        message = loadStrings.text.insufficient_balance
                        inline_options = InlineKeyboardMarkup([
                            [   
                                InlineKeyboardButton(loadStrings.callback_text.financial, callback_data= 'financial'),
                                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'newconfig')
                            ]
                        ])

                    resp_msg = await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
                    set_msg_id(chat_id, resp_msg.message_id, db)
                    return

                else:

                    resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_config, reply_markup= inline_options)
                    set_msg_id(chat_id, resp_msg.message_id, db)
                    continue
            
            if total_config != '***':
                config_number = total_config + count + 1
                if len(str(config_number)) == 1:
                    config_number = f'  {config_number}  '
                elif len(str(config_number)) == 2:
                    config_number = f' {config_number}  '
                elif len(str(config_number)) == 3:
                    config_number = f' {config_number} '
                elif len(str(config_number)) == 4:
                    config_number = f'{config_number} '

            username = resp.json()['username']
            password = resp.json()['password']
            host = resp.json()['host']
            port = resp.json()['port']

            inline_options = InlineKeyboardMarkup([
                [   
                    InlineKeyboardButton(loadStrings.callback_text.tick_for_understrike, callback_data= 'newconfig_tick'),
                ]
            ])

            config_text = loadStrings.text.config_text.format(host, port, username, password, config_number)
            await context.bot.send_message(chat_id= chat_id, text= config_text, parse_mode='markdown', reply_markup= inline_options)

        set_position(chat_id, 'mainmenu', db)
        await MenuManager().manager(update, context)


    async def click(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
           strike config 
        """
        query = update.callback_query
        sp_old_text = query.message.text.split('\n')

        new_text = []
        new_text.append(sp_old_text[0].replace('🔹', '▪', 2))

        for line in sp_old_text[1:]:
            main_line, strike_line = line.split(' ')
            new_text.append(f'{main_line} <s>{strike_line}</s>')

        join_text=  '\n'.join(new_text).strip()
        await query.edit_message_text(text= join_text, parse_mode='html')
