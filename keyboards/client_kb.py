########################################
#  Этот файл используется для создания #
#  разных клавиатур       !            #
########################################
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ----------------------Клавиатура 1----------------------------------------------
Button1 = KeyboardButton('👋 Поздороваться')
Button2 = KeyboardButton('🔓 Авторизоваться')
keyboards_client_step1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step1.row(Button1, Button2)  # add(Button1).add(Button2).insert(Button3)

# ----------------------Клавиатура 2----------------------------------------------
Button2 = KeyboardButton('🔓 Авторизоваться')
keyboards_client_step2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step2.row(Button2)  # add(Button1).add(Button2).insert(Button3)

# ----------------------Клавиатура 3----------------------------------------------
Button1 = KeyboardButton('💯 Оценки', callback_data="💯 Оценки")
Button2 = KeyboardButton('🕒 Расписание', callback_data="💯🕒 Расписание")
Button3 = KeyboardButton('📚 Домашнее задание', callback_data="📚 Домашнее задание")
Button4 = KeyboardButton('🚪 Разлогинится', callback_data="🚪 Разлогинится")
keyboards_client_step3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step3.row(Button1, Button2, Button3).add(Button4)  # add(Button1).add(Button2).insert(Button3)

# ----------------------Клавиатура 4----------------------------------------------
Button1 = InlineKeyboardButton(text='МАОУ Школа №16 г.Благовещенска',
                               callback_data='School_0')  # МАОУ "Школа № 16 г. Благовещенска"
Button2 = InlineKeyboardButton(text='МАОУ Школа №26 г.Благовещенска',
                               callback_data='School_1')  # МАОУ "Школа №26 г. Благовещенска"
Button3 = InlineKeyboardButton(text='МАОУ Гимназия №1 г.Благовещенска',
                               callback_data='School_2')  # МАОУ "Гимназия № 1 г. Благовещенска"
Button4 = InlineKeyboardButton(text='МАОУ Школа №28 г.Благовещенска',
                               callback_data='School_3')  # МАОУ "Школа №28 г. Благовещенска"
Button5 = InlineKeyboardButton(text='МАОУ Школа №27 г.Благовещенска',
                               callback_data='School_4')  # МАОУ "Школа №27 города Благовещенска"
Button6 = InlineKeyboardButton(text='МАОУ Школа №14 г.Благовещенска',
                               callback_data='School_5')  # МАОУ "Школа № 14 г. Благовещенска"
keyboards_client_step4 = InlineKeyboardMarkup(row_width=1)
keyboards_client_step4.add(Button1, Button2, Button3, Button4, Button5, Button6)

# ----------------------Клавиатура 5----------------------------------------------
Button1 = KeyboardButton('🔙 Вернуться')
Button2 = KeyboardButton('⬅️ Предыдущая')
Button3 = KeyboardButton('Текущая неделя')
Button4 = KeyboardButton('Следующая ➡️')
keyboards_client_step5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step5.row(Button2, Button3, Button4).row(Button1)
# ----------------------Клавиатура 6----------------------------------------------
Button1 = KeyboardButton('🔙.')
Button2 = KeyboardButton('ПН')
Button3 = KeyboardButton('ВТ')
Button4 = KeyboardButton('СР')
Button5 = KeyboardButton('ЧТ')
Button6 = KeyboardButton('ПТ')
Button7 = KeyboardButton('СБ')
keyboards_client_step6 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step6.row(Button2, Button3, Button4).row(Button5, Button6, Button7).row(Button1)
# ----------------------Клавиатура 7----------------------------------------------
Button1 = KeyboardButton('Продолжить')
keyboards_client_step7 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step7.row(Button1)
# ----------------------Клавиатура 8----------------------------------------------
Button1 = KeyboardButton('.🔙 Вернуться')
Button2 = KeyboardButton('.⬅️ Предыдущая')
Button3 = KeyboardButton('.Текущая неделя')
Button4 = KeyboardButton('.Следующая ➡️')
keyboards_client_step8 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step8.row(Button2, Button3, Button4).row(Button1)
# ----------------------Клавиатура 9----------------------------------------------
Button1 = KeyboardButton('.🔙.')
Button2 = KeyboardButton('.ПН')
Button3 = KeyboardButton('.ВТ')
Button4 = KeyboardButton('.СР')
Button5 = KeyboardButton('.ЧТ')
Button6 = KeyboardButton('.ПТ')
Button7 = KeyboardButton('.СБ')
keyboards_client_step9 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step9.row(Button2, Button3, Button4).row(Button5, Button6, Button7).row(Button1)
# ----------------------Клавиатура 10----------------------------------------------
Button1 = KeyboardButton('.🔙 Вернуться.')
Button2 = KeyboardButton('.⬅️ Предыдущая.')
Button3 = KeyboardButton('.Текущая неделя.')
Button4 = KeyboardButton('.Следующая ➡️.')
keyboards_client_step10 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step10.row(Button2, Button3, Button4).row(Button1)
# ----------------------Клавиатура 11----------------------------------------------
Button1 = KeyboardButton('🔙..')
Button2 = KeyboardButton('.ПН.')
Button3 = KeyboardButton('.ВТ.')
Button4 = KeyboardButton('.СР.')
Button5 = KeyboardButton('.ЧТ.')
Button6 = KeyboardButton('.ПТ.')
Button7 = KeyboardButton('.СБ.')
keyboards_client_step11 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboards_client_step11.row(Button2, Button3, Button4).row(Button5, Button6, Button7).row(Button1)
