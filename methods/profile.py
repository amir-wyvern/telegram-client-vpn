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
    set_msg_id,
    delete_cache
)
from utils.db_cache import db_cache
from api.profile import get_profile, claim_profit_via_wallet


class ProfileManager:

    @db_cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'profile': lambda: self.profile(update, context, db),
            'profile_profit_menu': lambda: self.profile_profit_menu(update, context, db),
            'profile_profit_via_wallet': lambda: self.get_profit_via_wallet(update, context, db),
            'profile_profit_via_withdraw': lambda: self.profile_profit_via_withdraw(update, context, db),
        }

        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()


    async def profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            show profile
        """
        chat_id = update.effective_chat.id

        delete_cache(chat_id, db)
        set_position(chat_id, 'profile', db)


        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.get_profit_text, callback_data= 'profile_profit_menu'),
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'mainmenu')
            ]
        ])


        session = get_session(chat_id, db)
        resp = get_profile(session)

        if resp.status_code != 200 :

            username= "***"
            referal_link= "***"
            percent_profit= "20%"
            not_released_profit= "***"
            total_profit= "***"
            subset_number_of_configs= "***"
            subset_limit= '***'
            subset_list= '***'

        else:

            data = resp.json()
            username= data['username']
            referal_link= data['referal_link']
            percent_profit= "20 درصد"
            subset_limit= data['subset_number_limit']
            not_released_profit= data['subset_not_released_profit']
            total_profit= data['subset_total_profit']
            subset_number_of_configs= data['subset_number_of_configs']
            subset_list= '* --- *'

            if data['subset_list']:
                subset_list = data['subset_list'][0]
                
                if len(data['subset_list']) > 1:
                    for agent in data['subset_list'][1]:
                        subset_list = f'{subset_list} | {agent}'

        text = loadStrings.text.profile_text.format(
            username, 
            referal_link, 
            percent_profit, 
            subset_limit, 
            not_released_profit,
            total_profit,
            subset_number_of_configs,
            subset_list
            )

        await update.callback_query.edit_message_text( text, reply_markup= inline_options, parse_mode='MARKDOWN')


    async def profile_profit_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.get_profit_via_wallet, callback_data= 'profile_profit_via_wallet')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.get_profit_via_withdraw, callback_data= 'profile_profit_via_withdraw')
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'profile')
            ]
        ])

        update.callback_query.edit_message_text(loadStrings.text.profit_menu, reply_markup= inline_options, parse_mode='MARKDOWN')


    async def get_profit_via_wallet(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id

        session = get_session(chat_id, db)

        resp = get_profile(session)

        if resp.status_code != 200 :
            inline_options = InlineKeyboardMarkup([
                        [   
                            InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                            InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'profile')
                        ]
                    ])
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return

        value = resp.json()['subset_not_released_profit']
        resp = claim_profit_via_wallet(session, value)
        
        if resp.status_code != 200:
            
            if resp.status_code in [409]:
                
                message = loadStrings.text.internal_error

                if resp.json()['detail']['internal_code'] == 2464:
                    message = loadStrings.text.error_not_have_profit


                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'profile')
                    ]
                ])

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)
                return

            else:
        
                inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
                        InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'profile')
                    ]
                ])

                resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error, reply_markup= inline_options)
                set_msg_id(chat_id, resp_msg.message_id, db)
                return

        success_text = loadStrings.text.claim_profit_success.format(value)
        resp_msg = await context.bot.send_message(chat_id= chat_id, text= success_text, reply_markup= inline_options)
        set_msg_id(chat_id, resp_msg.message_id, db)

        await ProfileManager().manager(update, context, edit= False)
    

    async def get_profit_via_withdraw(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        query = update.callback_query

        await query.answer(loadStrings.text.coming_soon)
        return
