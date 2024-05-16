from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .states import UserStates
from db.db import UserDb


class BaseMarkup:
    raw_buttons = {
        "back": {"back": "Назад ↩️"},
        'admin': {'create': 'Создать раздачу 🆕', 'mailing': 'Сделать рассылку 📧', 'active_task': 'Активная раздача 🔥'},
        'user': {'order': 'Записаться на Раздачу 📝'},
        'done': {'done': 'Я выполнил условия ✅'},
        'refresh': {'refresh': 'Обновить 🔄'},
        'all': {'all': 'Всем 🌍'},
        'task': {'task': 'Участники: {task} 👥'},
        'create': {'create_title': 'Название 📝',
                   'create_text': 'Описание 📄',
                   'create_photo': 'Фото 📷',
                   'create_goal': 'Условие 🎯',
                   'done_text': "Текст выполнено 📝",
                   'send': 'Создать 🚀'},
        'delete_task': {'delete_task': 'Удалить раздачу ❌'},
        'desc_mailing': {'text': 'Текст 📝', 'photo': 'Фото 📷'},
        'creating_mail': {'create_mailing_text': 'Текст для рассылки 📝', 'create_mailing_photo': 'Фото для рассылки 📷',
                          'send_mailing': 'Отправить рассылку 📤'}
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
            if key == 'send' and count != 5:
                continue
            buttons[key] = value
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(*self._gen_markup(buttons)).add(*self._gen_markup(self.raw_buttons['back']))
        return keyboard

    async def create_mailing(self, state):
        data_state = await state.get_data()
        buttons = {}
        count = 0
        for key, value in self.raw_buttons['creating_mail'].items():
            if data_state.get(key):
                count += 1
                value = value + '✅'
            if key == 'send_mailing' and count != 2:
                continue
            buttons[key] = value
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(*self._gen_markup(buttons)).add(*self._gen_markup(self.raw_buttons['back']))
        return keyboard

    async def task_actions(self, user_id):
        db = UserDb()
        task = db.active_tasks()
        user_inviters = db.user_task([user_id, task[0]])
        if user_inviters[1] >= task[4]:
            return self.get_markup('done', columns=2)
        return self.get_markup('refresh', columns=2)

    async def type_mailing(self):
        db = UserDb()
        task = db.active_tasks()
        keyboard = InlineKeyboardMarkup(row_width=2)
        users = self._gen_markup(self.raw_buttons['all'])
        if task:
            active_task = self.raw_buttons['task']
            active_task['task'] = active_task['task'].format(task=task[1])
            users += self._gen_markup(active_task)
        keyboard.add(*users)
        return keyboard


class BaseText:
    stock = {
        "admin_start": "Привет, админ 👋",
        'create': 'Отправьте параметры для создания задачи. ✉️',
        'send_task': 'Задача успешно сохранена. 🎉',
        'del_task': 'Раздача удалена. ❌',
        'task_info': 'Здесь находится информация о раздаче. 📋',
        'mailing': 'Рассылка. 📧',
        'mailing_creating': 'Создание рассылки. 📤',
        'start_mail': "Начинаю рассылку, доступных пользователей: {users}. 🚀"
    }

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
            case 'done_text':
                return 'Укажите текст который будет отправлен после выполнения раздачи:'

    @staticmethod
    async def creating_mail(state):
        data_state = await state.get_data()
        step = data_state.get('creating_mail_step')
        match step:
            case 'create_mailing_text':
                return 'Введите текст рассылки:'
            case 'create_mailing_photo':
                return 'Добавьте фото:'


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
                         'done_text': self._creating,
                         'send': self._ready,
                         'active_task': self._active_task,
                         'delete_task': self._delete_task,
                         'back': self._back,
                         'order': self._refresh,
                         'refresh': self._refresh,
                         'all': self._type_mailing,
                         'task': self._type_mailing,
                         'create_mailing_text': self._create_mailing,
                         'create_mailing_photo': self._create_mailing,
                         'send_mailing': self._back,

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
            "text": self.text.stock.get("mailing"),
            "reply_markup": await self.type_mailing(),
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

    async def _refresh(self):
        task = self.db.active_tasks()
        user_inviters = self.db.user_task([self.call.from_user.id, task[0]])
        ref_link = f'https://t.me/EasyLife_test_bot?start={self.call.from_user.id}-{task[0]}'
        text = (f'Название: {task[1]}\n\nОписание: {task[2]}\nЦель: {user_inviters[1]}/{task[4]}\n'
                f'Пригласительная ссылка: `{ref_link}`')
        return {
            "text": text,
            "reply_markup": await self.task_actions(self.call.from_user.id),
            'photo': task[3]}

    async def _type_mailing(self):
        await self.state.update_data(**{'type_mailing': self.call.data})
        return {
            "text":  self.text.stock.get('mailing_creating'),
            'reply_markup': await self.create_mailing(self.state),
            "state": UserStates.create_mail}

    async def _create_mailing(self):
        await self.state.update_data(**{'creating_mail_step': self.call.data})
        state = UserStates.create_mail
        if self.call.data == 'create_mailing_photo':
            state = UserStates.mail_photo
        return {
            "text": await self.text.creating_mail(self.state),
            "state": state}
