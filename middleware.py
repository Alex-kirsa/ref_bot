from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dispather import bot, dp

chanel_id = -1002093034927
chanel_url = 'https://t.me/tteett221'


class BlockMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        chat1 = await message.bot.get_chat_member(chat_id=chanel_id, user_id=message.from_user.id)
        if chat1.status == "member" or chat1.status == "administrator" or chat1.status == "creator":
            pass
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(text="Подписаться", url=chanel_url))
            await bot.send_message(message.from_user.id, 'Что бы продолжить Вам нужно подписаться на канал:',
                                   reply_markup=keyboard
                                   )
            raise CancelHandler()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        chat1 = await callback_query.bot.get_chat_member(chat_id=chanel_id,
                                                         user_id=callback_query.from_user.id)
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="Подписаться", url=chanel_url))
        if chat1.status == "member" or chat1.status == "administrator" or chat1.status == "creator":
            pass
        else:
            await bot.send_message(callback_query.from_user.id, 'Что бы продолжить Вам нужно подписаться на канал:',
                                   reply_markup=keyboard
                                   )
            raise CancelHandler()


dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(BlockMiddleware())
