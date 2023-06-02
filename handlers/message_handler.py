from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram import Update

from lang import loadStrings
from api import services



async def show_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    tel_id = update.effective_chat.id

    plans = services.get_all_services()

    ls_button = []

    for plan in plans:
        if hasattr(loadStrings.button, plan.replace('_plan', '')):
            ls_button.append(KeyboardButton(getattr(loadStrings.button,  plan.replace('_plan', ''))))

    options = ReplyKeyboardMarkup([ls_button], resize_keyboard=True)

    await context.bot.send_message(chat_id= tel_id, text= loadStrings.list_plan_text, reply_markup=options)


async def detail_plan(update: Update, context: ContextTypes.DEFAULT_TYPE, plan):
    
    tel_id = update.effective_chat.id

    ssh_plans = services.get_ssh_services()
    
    ls_inline_keyboards = []
    
    for ssh_plan in ssh_plans:
        if loadStrings.getattr(loadStrings.command, '{0}unlimit_{1}d_{2}user_plan'.format('', plan['duration'], plan['limit'])) == plan:
            
            trafic = 'نامحدود' if ssh_plan['trafic'] == 0 else ssh_plan['trafic'] 

            ls_inline_keyboards.append(
                InlineKeyboardButton(loadStrings.text.wallet_payment, callback_data='service_ssh_{0}'.format(ssh_plan['interface_id']))
            )
            
            options = InlineKeyboardMarkup([ls_inline_keyboards])
            await context.bot.send_message(chat_id= tel_id, text= loadStrings.text.plan_detail.format('ssh', trafic, ssh_plan['limit'], ssh_plan['price']), reply_markup=options)
            

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    messages_pointer = {
        loadStrings.button.buy_vpn: lambda : show_plans(update, context),
        loadStrings.button.unlimit_30d_2user: lambda : detail_plan(update, context, loadStrings.command.unlimit_30d_2user),
        loadStrings.button.unlimit_60d_2user: lambda : detail_plan(update, context, loadStrings.command.unlimit_60d_2user),
        loadStrings.button.unlimit_30d_1user: lambda : detail_plan(update, context, loadStrings.command.unlimit_30d_1user),
        loadStrings.button.unlimit_60d_1user: lambda : detail_plan(update, context, loadStrings.command.unlimit_60d_2user)
        # loadStrings.button.ssh_unlimit_30d: lambda : detail_plan(update, context, loadStrings.button.unlimit_30d_2user),
    }

    positions_pointer = {
        # 'menu': lambda : menu(update, context),
    }
    if update.message.text in messages_pointer:

        await messages_pointer[update.message.text]()
    
    # elif user['pos'] in positions_pointer:

    #     await positions_pointer[user['pos']]()

