#######################################
#  Этот файл используется для запуска #
#  работы телеграмм-бота!             #
#######################################
from aiogram.utils import executor  # Импорт скрипта запуска из библиотеки aiogram

from create_bot import dp, bot
from handlers import clients, other


# Функция - при полном запуске программы отправляет сообщение
async def on_startup(_):
    print('Бот вышел в онлайн')
    await bot.delete_webhook(drop_pending_updates=True)  # Функция удаление всех событий до включения бота


clients.registration_handler_client(dp)  # Функция Регистрации Диспетчеров-обработчиков из файла клиент
other.registration_handler_other(dp)  # Функция Регистрации Диспетчеров-обработчиков из файла остальные

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # Функция запуска бота
