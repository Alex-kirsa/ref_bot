from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from dispather import dp, bot
from dispather import LIST_ADMINS
from major import UserStates, UserManager
import hendlers
import middleware


@dp.message_handler(commands=["start"], state=['*'])
async def start(msg: types.Message, state: FSMContext):
    manager = UserManager()
    # ref = msg.text.split(" ")
    # inviter = 0
    # if len(ref) >= 2:
    #     inviter = ref[1].split('-')
    #     task = inviter[1]
    #     inviter = inviter[0]
    #     manager.db.add_referral_task(msg.from_user.id, task, inviter)
    # if not await manager.db.check_user(inviter):
    #     inviter = 0
    # user = {'id': msg.from_user.id, 'invited_by': inviter, 'username': msg.from_user.username}
    # await manager.db.init_user_db(user)
    if msg.from_user.id in LIST_ADMINS:
        await msg.answer(manager.text.stock['admin_start'], reply_markup=manager.buttons.get_markup('admin', columns=2),)
        await UserStates.admin.set()
        return
    task = manager.db.active_tasks()
    if task:
        user_inviters = manager.db.user_task([msg.from_user.id, task[0]])
        buttons = manager.buttons.get_markup('user')
        if user_inviters[1] < task[4]:
            if user_inviters[0]:
                buttons = await manager.buttons.task_actions(msg.from_user.id)
            ref_link = f'https://t.me/bonus_1win_vaucher_bot?start={msg.from_user.id}-{task[0]}'
            text = (f'Название: {task[1]}\n\nОписание: {task[2]}\nЦель: {user_inviters[1]}/{task[4]}\n'
                    f'Пригласительная ссылка: <code>{ref_link}</code>')
            await bot.send_photo(msg.from_user.id,
                                 photo=task[3],
                                 caption=text,
                                 reply_markup=buttons,)
            return
        else:
            await msg.answer(task[-1],)
            return

    await msg.answer(manager.text.stock.get('task_info'))
    await UserStates.user.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
