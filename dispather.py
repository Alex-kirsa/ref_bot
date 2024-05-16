from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher


storage = MemoryStorage()

TOKEN = '7100750803:AAESFIRhXP4kasVrnmGJTFPpUrtRuXs0GYA'

LIST_ADMINS = (6133947978,5759412217)

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

