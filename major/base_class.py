from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .states import UserStates
from db.db import UserDb


class BaseMarkup:
    raw_buttons = {
        "back": {"back": "Назад"},
        'admin': {'create': 'Создать раздачу', 'mailing': 'Сделать рассылку', 'active_task': 'Активная раздача'},
        'user': {'': 'Записаться на Раздачу'},
        'info_task': {'info_task': 'Узнать о раздаче'},
        'done': {'done': 'Я выполнил условия'},
        'refresh': {'refresh': 'обновить '},
        'type_mailing': {'all': 'Всем', 'task': 'участники: {task}'},
        'create': {'create_title': 'Название',
                   'create_text': 'Описание',
                   'create_photo': 'Фото',
                   'create_goal': 'Условие',
                   'send': 'Создать'},
        'delete_task': {'delete_task': 'Удалить раздачу'},
        'desc_mailing': {'text': 'текст', 'photo': 'фото'},
        'send_mailing': {'send_mailing': 'Отправить'},
    }

    @staticmethod
    def _gen_markup(data: dict) -> list:
        """
        accepts dict and generate InlineKeyboardMarkups
        :param data:dict
        :return: list InlineKeyboardMarkups
        """
        return [
            InlineKeyboardButton(text=text, callback_data=callback)
            for callback, text in data.items()
        ]

    def get_markup(self, *args: str, columns=1) -> InlineKeyboardMarkup:
        """
        accepts str and return keyboard with buttons
        :param columns:
        :param markup:
        :return: InlineKeyboardMarkups
        """
        buttons = [self.raw_buttons.get(but, {}) for but in args]
        keyboard = InlineKeyboardMarkup(row_width=columns)
        keyboard_list = []
        for markup in buttons:
            for callback, text in markup.items():
                keyboard_list.append(InlineKeyboardButton(text=text,
                                                          callback_data=callback))
        keyboard.add(*keyboard_list)
        return keyboard

    async def create_task(self, state):
        data_state = await state.get_data()
        buttons = {}
        count = 0
        for key, value in self.raw_buttons['create'].items():
            if data_state.get(key):
                count += 1
                value = value + '✅'
            if key == 'send' and count != 4:
                continue
            buttons[key] = value
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(*self._gen_markup(buttons)).add(*self._gen_markup(self.raw_buttons['back']))
        return keyboard


class BaseText:
    stock = {
        "admin_start": "Hi admin",
        'create': 'send params for create task',
        'send_task': 'successful save new task',
        'del_task': 'Раздача удалена'}

    @staticmethod
    async def creating(state):
        data_state = await state.get_data()
        step = data_state.get('creating_step')
        match step:
            case 'create_title':
                return 'Введите название:'
            case 'create_text':
                return 'Введите описание:'
            case 'create_photo':
                return 'Отправьте фото:'
            case 'create_goal':
                return 'Укажите количество подписчиков:'


class Buttons(BaseMarkup):
    def __init__(self, state, call=None):
        self.state = state
        self.call = call
        self.db = UserDb()
        self.data_but = {"create": self._create,
                         "mailing": self._mailing,
                         'create_title': self._creating,
                         'create_text': self._creating,
                         'create_photo': self._creating,
                         'create_goal': self._creating,
                         'send': self._ready,
                         'active_task': self._active_task,
                         'delete_task': self._delete_task,
                         'back': self._back

                         }
        self.text = BaseText()

    async def _create(self):
        return {
            "text": self.text.stock.get("create"),
            "reply_markup": await self.create_task(self.state),
            "state": UserStates.create}

    async def _ready(self):
        data_state = await self.state.get_data()
        task_info = [data_state.get(key) for key in self.raw_buttons['create'].keys()]
        self.db.add_task(*task_info[:-1])
        await self.state.finish()
        return {
            "text": self.text.stock.get("admin_start"),
            "reply_markup": self.get_markup('admin', columns=2),
            "state": UserStates.admin}

    async def _mailing(self):
        return {
            "text": self.text.stock.get("welcome"),
            "reply_markup": '2123',
            "state": UserStates.mailing}

    async def _creating(self):
        await self.state.update_data(**{'creating_step': self.call.data})
        state = UserStates.create
        if self.call.data == 'create_photo':
            state = UserStates.photo
        return {
            "text": (await self.text.creating(self.state)),
            "state": state}

    async def _active_task(self):
        task = self.db.active_tasks()
        if task:
            text = f'Название: {task[1]}\n\nОписание: {task[2]}\nЦель:{task[4]}'
            return {
                "text": text,
                "state": UserStates.task,
                'photo': task[3],
                "reply_markup": self.get_markup('delete_task', 'back')}
        return {
            "text": "Сейчас нет активных раздач",
            "reply_markup": self.get_markup('back')}

    async def _delete_task(self):
        self.db.del_task()
        return {
            "text": self.text.stock.get("admin_start"),
            "reply_markup": self.get_markup('admin', columns=2),
            "state": UserStates.admin}

    async def _back(self):
        await self.state.finish()
        return {
            "text": self.text.stock.get("admin_start"),
            "reply_markup": self.get_markup('admin', columns=2),
            "state": UserStates.admin}