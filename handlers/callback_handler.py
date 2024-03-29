from telegram.ext import ContextTypes
from telegram import Update
from utils.db_cache import db_cache
from methods.new_config import NewConfigManager
from methods.login import LoginManager
from methods.menu import MenuManager
from methods.manage_users import ManageUsersManager
from methods.update_expire import UpdateExpireConfigManager
from methods.renew_config import RenewConfigManager
from methods.user_status import UserStatusManager
from methods.block_user import BlockUserManager
from methods.unblock_user import UnBlockUserManager
from methods.help import HelpManager
from methods.financial import FinancialManager
from methods.test_config import TestConfigManager
from methods.delete_user import DeleteUserManager
from methods.profile import ProfileManager
from methods.notification import NotificationManager
import logging

logger = logging.getLogger('callback_handler.log') 
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('callback_handler.log') 
file_handler.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s') 
file_handler.setFormatter(formatter) 
logger.addHandler(file_handler) 

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


newConfigManager = NewConfigManager()
loginManager = LoginManager()
mainmenu = MenuManager()
manageUsers = ManageUsersManager()
updateExpire = UpdateExpireConfigManager()
renewConfig = RenewConfigManager()
userStatus = UserStatusManager()
blockUser = BlockUserManager()
unblockUser = UnBlockUserManager()
help = HelpManager()
financial = FinancialManager()
deleteUser = DeleteUserManager()
testConfig = TestConfigManager()
profile = ProfileManager()
notification = NotificationManager()

@db_cache
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    
    
    query = update.callback_query
    # Acknowledge the button click and send a response

    callback_poitner = {
        'login' : lambda : loginManager.manager(update, context, edit= True),
        'newconfig' : lambda : newConfigManager.manager(update, context),
        'testconfig' : lambda : testConfig.manager(update, context),
        'mainmenu' : lambda : mainmenu.manager(update, context, edit=True),
        'manageusers': lambda: manageUsers.manager(update, context, edit=True),
        'updateexpire': lambda: updateExpire.manager(update, context, edit=True),
        'renewconfig': lambda: renewConfig.manager(update, context, edit=True),
        'userstatus': lambda: userStatus.manager(update, context, edit=True),
        'blockuser': lambda: blockUser.manager(update, context, edit=True),
        'deleteuser': lambda: deleteUser.manager(update, context, edit=True),
        'unblockuser': lambda: unblockUser.manager(update, context, edit=True),
        'financial': lambda: financial.manager(update, context, edit=True),
        'profile': lambda: profile.manager(update, context, edit=True),
        'notif': lambda: notification.manager(update, context, edit=True),
        'help': lambda: help.manager(update, context, edit=True)
    }
    
    if query.data.split('_')[0] in callback_poitner:
        await callback_poitner[query.data.split('_')[0]]()

    # query = update.callback_query
    # tel_id = query.message.chat.id

    # await query.answer()

    # callback_pointer = {
    #     'service' : lambda : buy_service(update, context)
    # }

    # key = query.data.split('_')[0]

    # if key in callback_pointer:
    #     await callback_pointer[key]()

