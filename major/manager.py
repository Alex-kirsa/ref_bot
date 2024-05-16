import aiogram.utils.exceptions

from .base_class import Buttons, BaseText
from db.db import UserDb
from dispather import bot


class Msg(Buttons):
    def __init__(self, call, state):
        super().__init__(state)
        self.call = call
        self.chat_id = call.message.chat.id
        self.msg_id = call.message.message_id

    data_mapping = {}

    async def _send(self, ):
        if self.data_mapping.get('photo'):
            await self.call.message.delete()
            # with open(f'General/media/{self.data_mapping["photo"]}.png', "rb") as photo:
            await bot.send_photo(self.chat_id,
                                 photo=self.data_mapping['photo'],
                                 caption=self.data_mapping['text'],
                                 reply_markup=self.data_mapping['reply_markup'],)
        elif self.data_mapping.get('reply_markup'):
            try:
                await bot.edit_message_text(
                    self.data_mapping['text'],
                    self.chat_id,
                    self.msg_id,
                    reply_markup=self.data_mapping['reply_markup'])
            except aiogram.utils.exceptions.BadRequest:
                await self.call.message.delete()
                await bot.send_message(self.chat_id,
                                       self.data_mapping['text'],
                                       reply_markup=self.data_mapping['reply_markup'])
        else:
            await bot.edit_message_text(
                self.data_mapping['text'],
                self.chat_id,
                self.msg_id)

    async def answer(self):
        if self.call.data in self.data_but:
            but = self.call.data
            self.data_mapping = await self.data_but[but]()
            await self._send()
            if self.data_mapping.get('state'):
                await self.data_mapping['state'].set()


class UserManager:
    def __init__(self, call=None, state=None):
        self.text = BaseText()
        self.buttons = Buttons(state, call)
        self.db = UserDb()
        if call:
            self.msg = Msg(call, state)
            self.call = call
