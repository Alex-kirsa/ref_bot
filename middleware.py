from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dispather import bot, dp
from major import UserManager

chanel_id = -1002014371596
chanel_url = 'https://t.me/+xoB1r2ptGt8yNGVi'


class BlockMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        manager = UserManager()
        try:
            ref = message.text.split(" ")
            inviter = 0
            if len(ref) >= 2:
                inviter = ref[1].split('-')
                task = inviter[1]
                inviter = inviter[0]
                manager.db.add_referral_task(message.from_user.id, task, inviter)
            if not await manager.db.check_user(inviter):
                inviter = 0
            user = {'id': message.from_user.id, 'invited_by': inviter, 'username': message.from_user.username}
            await manager.db.init_user_db(user)
        except AttributeError:
            pass
        chat1 = await message.bot.get_chat_member(chat_id=chanel_id, user_id=message.from_user.id)
        if chat1.status == "member" or chat1.status == "administrator" or chat1.status == "creator":
            pass
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(text="Подписаться", url=chanel_url),
                         InlineKeyboardButton(text="Обновить", callback_data='update'))
            await bot.send_message(message.from_user.id, 'Что бы продолжить Вам нужно подписаться на канал:',
                                   reply_markup=keyboard
                                   )
            raise CancelHandler()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        chat1 = await callback_query.bot.get_chat_member(chat_id=chanel_id,
                                                         user_id=callback_query.from_user.id)
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="Подписаться", url=chanel_url),
                     InlineKeyboardButton(text="Обновить", callback_data='update'))
        if chat1.status == "member" or chat1.status == "administrator" or chat1.status == "creator":
            pass
        else:
            await bot.send_message(callback_query.from_user.id, 'Что бы продолжить Вам нужно подписаться на канал:',
                                   reply_markup=keyboard
                                   )
            raise CancelHandler()


dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(BlockMiddleware())
