from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher


storage = MemoryStorage()

TOKEN = '6607850427:AAGpmWl0homidZ-M2gVy7Sk-ZQ-9zzbpFHg'

LIST_ADMINS = (6133947978,)

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

