from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from dispather import dp
from dispather import LIST_ADMINS
from major import UserStates, UserManager
import hendlers
import middleware


@dp.message_handler(commands=["start"], state=['*'])
async def start(msg: types.Message, state: FSMContext):
    manager = UserManager()
    ref = msg.text.split(" ")
    inviter = 0
    if len(ref) >= 2:
        inviter = ref[1]
    if not await manager.db.check_user(inviter):
        inviter = 0
    user = {'id': msg.from_user.id, 'invited_by': inviter, 'username': msg.from_user.username}
    await manager.db.init_user_db(user)
    if msg.from_user.id in LIST_ADMINS:
        await msg.answer(manager.text.stock['admin_start'], reply_markup=manager.buttons.get_markup('admin', columns=2))
        await UserStates.admin.set()
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
