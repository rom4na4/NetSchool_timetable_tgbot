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
