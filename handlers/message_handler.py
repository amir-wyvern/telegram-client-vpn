
from telegram import Update
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
from cache.cache_session import get_position, set_msg_id
from utils.msg_delete import msg_delete, one_delete_msg

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
        'updateexpire': lambda: updateExpire.manager(update, context, edit= False),
        'renewconfig': lambda: renewConfig.manager(update, context, edit= False),
        'userstatus': lambda: userStatus.manager(update, context, edit=False),
        'blockuser': lambda: blockUser.manager(update, context, edit=False),
        'unblockuser': lambda: unBlockUser.manager(update, context, edit=False)
    }

    # its used for manage delete message_id, if a msg_id exist in this pos , that msg_id dont delete directly
    used_for_msg = [
        'blockuser_get_username',
        'login_get_username',
        'login_get_password',
        'renewconfig_get_username',
        'unblockuser_get_username',
        'blockuser_get_username',
        'updateexpire_get_username',
        'userstatus_get_username'
    ]

    if pos in used_for_msg:
        set_msg_id(chat_id, update.message.message_id, db)
        await msg_delete(chat_id, db)

    else: 
        await one_delete_msg(chat_id, update.message.message_id)

    if pos.split('_')[0] in messages_pointer:
        await messages_pointer[pos.split('_')[0]]()



