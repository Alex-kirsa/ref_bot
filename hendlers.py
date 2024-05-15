from aiogram import types
from aiogram.dispatcher import FSMContext
import requests
from dispather import dp, bot
from major import UserManager, UserStates


@dp.callback_query_handler(lambda call: True, state=['*'])
async def but_filter(call: types.CallbackQuery, state: FSMContext):
    manager = UserManager(call, state)
    match call.data:
        case 'send':
            await call.answer(manager.text.stock.get('send_task'), show_alert=True)
        case 'delete_task':
            await call.answer(manager.text.stock.get('del_task'), show_alert=True)

    await manager.msg.answer()


@dp.message_handler(content_types=["text"], state=UserStates.create)
async def creating(msg: types.Message, state: FSMContext):
    manager = UserManager(state=state)
    data_state = await state.get_data()
    step = data_state.get('creating_step')
    await state.update_data(**{step: msg.text})
    await msg.answer(manager.text.stock.get('create'), reply_markup=await manager.buttons.create_task(state))


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
