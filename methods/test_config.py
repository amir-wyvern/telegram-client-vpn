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
    get_session,
    set_msg_id
)
from utils.db_cache import db_cache
from api.services import buy_test_ssh_service
from methods.menu import MenuManager


class TestConfigManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            manager requests this methods 
        """
        query = update.callback_query
    
        self.pointer = {
            'testconfig': lambda : self.submit(update, context, db),
            'testconfig_tick': lambda : self.click(update, context, db),
        }
    
        if query.data in self.pointer:
            await self.pointer[query.data]()


    async def submit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
           send request to server for get new config
        """
        query = update.callback_query
        chat_id = query.message.chat_id

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

        resp = buy_test_ssh_service(session)

        if resp.status_code != 200 :

            inline_options = InlineKeyboardMarkup([
                [   
                    InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                    InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
                ]
            ])

            if resp.status_code in [404, 409]:
            
                message = loadStrings.text.internal_error
            
                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
                    ]
                ])

                if resp.json()['detail']['internal_code'] == 2450:
                    message = loadStrings.text.error_no_server

                if resp.json()['detail']['internal_code'] == 2459:
                    message = loadStrings.text.reach_max_test

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)
                return

            else:

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_config, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)

        username = resp.json()['username']
        password = resp.json()['password']
        host = resp.json()['host']
        port = resp.json()['port']

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.tick_for_understrike, callback_data= 'testconfig_tick'),
            ]
        ])

        config_text = loadStrings.text.test_config_text.format(host, port, username, password)
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
        new_text.append(sp_old_text[0].replace('⏳', '▪', 2))

        for line in sp_old_text[1:]:
            main_line, strike_line = line.split(' ')
            if main_line == 'username:':
                new_text.append(f'{main_line} <code>{strike_line}</code>')
                continue
            new_text.append(f'{main_line} <s>{strike_line}</s>')

        join_text=  '\n'.join(new_text).strip()
        await query.edit_message_text(text= join_text, parse_mode='html')
