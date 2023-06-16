
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram import Update

from methods.login import LoginManager
from methods.manage_users import ManageUsersManager
from methods.update_expire import UpdateExpireConfigManager
from methods.renew_config import RenewConfigManager
from methods.user_status import UserStatusManager
from methods.block_user import BlockUserManager
from methods.unblock_user import UnBlockUserManager

from utils.db_cache import db_cache
from cache.cache_session import get_position


loginManager = LoginManager()
manageUsers = ManageUsersManager()
updateExpire = UpdateExpireConfigManager()
renewConfig = RenewConfigManager()
userStatus = UserStatusManager()
blockUser = BlockUserManager()
unBlockUser = UnBlockUserManager()

@db_cache
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    
    chat_id = update.effective_chat.id
    pos = get_position(chat_id, db)
    
    messages_pointer = {
        'login': lambda : loginManager.manager(update, context),
        'manageusers': lambda: manageUsers.manager(update, context, edit= False),
        'updateexpire': lambda: updateExpire.manager(update, context, edit= False),
        'renewconfig': lambda: renewConfig.manager(update, context, edit= False),
        'userstatus': lambda: userStatus.manager(update, context, edit=False),
        'blockuser': lambda: blockUser.manager(update, context, edit=False),
        'unblockuser': lambda: unBlockUser.manager(update, context, edit=False)
    }
    
    if pos.split('_')[0] in messages_pointer:
        await messages_pointer[pos.split('_')[0]]()

    # positions_pointer = {
    #     # 'menu': lambda : menu(update, context),
    # }
    # if update.message.text in messages_pointer:

    #     await messages_pointer[update.message.text]()
    
    # # elif user['pos'] in positions_pointer:

    # #     await positions_pointer[user['pos']]()

