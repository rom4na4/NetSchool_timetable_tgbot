#######################################################
#  Это САМЫЙ ВАЖНЫЙ ФАЙЛ! Без него бот не запустится! #
#  Это тело телеграмм бота для поддержки NetSchool!   #
#  Тут происходит сборка и запуск бота!               #
#######################################################

import os  # Импорт библиотеки работы с системой

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт библиотеки работы с хранилищем данных
from aiogram.dispatcher import Dispatcher

storage = MemoryStorage()  # Создание экземпляра класса хранилища

bot = Bot(token=os.getenv('TOKEN'))  # Токен разработчика - без него бот не будет работать
dp = Dispatcher(bot, storage=storage)  # Создаем главного диспетчера с хранилищем!
