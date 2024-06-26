from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    admin = State()
    create = State()
    mailing = State()
    photo = State()
    task = State()
    user = State()
    create_mail = State()
    mail_photo = State()
