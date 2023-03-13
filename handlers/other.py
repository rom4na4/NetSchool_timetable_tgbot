######################################################
#  Этот файл используется для работы над сообщениями #
#  без определенного обработчика!                    #
######################################################
from aiogram import types, Dispatcher


# Функция ответа на не распознанный текст
async def no_recognize(message: types.Message):  #
    await message.answer("Не понял вас! Следуйте инструкции пожалуйста!", parse_mode="Markdown")


def registration_handler_other(dp: Dispatcher):
    dp.register_message_handler(no_recognize)
