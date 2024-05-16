from aiogram import types
from aiogram.dispatcher import FSMContext
import requests
from dispather import dp, bot
from major import UserManager, UserStates
from common import send_mailing


@dp.callback_query_handler(lambda call: True, state=['*'])
async def but_filter(call: types.CallbackQuery, state: FSMContext):
    manager = UserManager(call, state)
    if call.data == 'send':
        await call.answer(manager.text.stock.get('send_task'), show_alert=True)
    elif call.data == 'delete_task':
        await call.answer(manager.text.stock.get('del_task'), show_alert=True)
    elif call.data == 'send_mailing':
        data_state = await state.get_data()
        type_mailing = data_state.get('type_mailing')
        if type_mailing == 'all':
            user_ids = manager.db.mailing()
        else:
            user_ids = manager.db.mailing(manager.db.active_tasks()[0])
        await bot.send_message(call.from_user.id, manager.text.stock.get('start_mail').format(users=len(user_ids)))
        result = await send_mailing(user_ids,
                                    [data_state.get('create_mailing_photo'), data_state.get('create_mailing_text')])
        await call.answer(f'Рассылка завершенна. Отправленно {result}/{len(user_ids)}', show_alert=True)
        await bot.send_message(call.from_user.id, manager.text.stock['admin_start'],
                               reply_markup=manager.buttons.get_markup('admin', columns=2))
        return
    elif call.data == 'done':
        task = manager.db.active_tasks()
        user_inviters = manager.db.user_task([call.from_user.id, task[0]])
        if user_inviters[1] >= task[4]:
            await bot.send_message(call.from_user.id, task[-1], parse_mode='MarkdownV2')
            return
    await manager.msg.answer()


@dp.message_handler(content_types=["text"], state=UserStates.create)
async def creating(msg: types.Message, state: FSMContext):
    manager = UserManager(state=state)
    data_state = await state.get_data()
    step = data_state.get('creating_step')
    await state.update_data(**{step: msg.text})
    await msg.answer(manager.text.stock.get('create'), reply_markup=await manager.buttons.create_task(state))


@dp.message_handler(content_types=["text"], state=UserStates.create_mail)
async def creating(msg: types.Message, state: FSMContext):
    manager = UserManager(state=state)
    data_state = await state.get_data()
    step = data_state.get('creating_mail_step')
    await state.update_data(**{step: msg.text})
    await msg.answer(manager.text.stock.get('mailing_creating'),
                     reply_markup=await manager.buttons.create_mailing(state), )


@dp.message_handler(content_types=["photo"], state=UserStates.photo)
async def save_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    manager = UserManager(state=state)
    data_state = await state.get_data()
    step = data_state.get('creating_step')
    await state.update_data(**{step: file_id})
    await message.answer(manager.text.stock.get('create'), reply_markup=await manager.buttons.create_task(state))
    await UserStates.create.set()


@dp.message_handler(content_types=["photo"], state=UserStates.mail_photo)
async def save_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    manager = UserManager(state=state)
    data_state = await state.get_data()
    step = data_state.get('creating_mail_step')
    await state.update_data(**{step: file_id})
    await message.answer(manager.text.stock.get('mailing_creating'),
                         reply_markup=await manager.buttons.create_mailing(state))
    await UserStates.create_mail.set()
