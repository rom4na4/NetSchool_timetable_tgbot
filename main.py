#Библиотека для работы с ботом телеграм
import telebot                                               # библиотека бота
import asyncio                                               # библиотека запросов
import json
from telebot import types
from netschoolapi import NetSchoolAPI

#Токен разработчика
bot = telebot.TeleBot('')

#Стандартный класс пользователя
class User:
    id = 0                                                       # id пользователя
    userlogin = ''                                               # Логин
    password = ''                                                # Пароль
    schoolname = ''                                              # Название школы
    diary = ''                                                   # Последние данные из дневника
    last_message = ''                                            # Последняя команда

    #Подключение к сетевому городу
    async def login(self, password, schoolname):
        ns = NetSchoolAPI('https://region.obramur.ru')               # Создаём клиент. Через него мы будем обращаться к АПИ электронного дневника
        await ns.login(self, password, schoolname)              # Логинимся

    # разлогиним телеграмм бота
    async def logout(self):
        ns = NetSchoolAPI('https://region.obramur.ru')               # Создаём клиент. Через него мы будем обращаться к АПИ электронного дневника
        await ns.logout()                                            # Разлогиниться - обязательно!

user_data = {
  "id": User.id,
  "username": User.userlogin,
  "password": User.password,
  "schoolname": User.schoolname,
  "diary": User.diary,
  "last_message": User.last_message
}

# with open("data/data.json", "w") as write_file:
#     json.dump(user_data, write_file, indent=4)
#
# with open("data/data.json", "r") as read_file:
#     user_data2 = json.load(read_file)

#Слушаем команды от клиента
@bot.message_handler(commands=['start', 'help'])
def start(message): #Функция по команде старт
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Создать клавиатуру для вывода кнопок
    btn1 = types.KeyboardButton("👋 Поздороваться") #Кнопка 1
    btn2 = types.KeyboardButton("Авторизоваться") #Кнопка 2
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник в сетевом городе!", reply_markup=markup)
    bot.send_message(message.from_user.id, "Я могу присылать тебе текущее Домашнее задание, Расписание и последние оценки по предметам ", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться':
        bot.send_message(message.from_user.id, 'И тебе привет! Хватит терять время! Чтобы получить данные, сначала <b>авторизуйся!</b>',parse_mode='html')
    elif message.text == 'Авторизоваться':
        msg = bot.send_message(message.from_user.id, 'Пока я авторизируюсь автоматически, но скоро я буду запрашивать информацию об авторизации у пользователя ', parse_mode='Markdown')
        try:
            #asyncio.run(User.login(User.userlogin, User.password, User.schoolname))
            asyncio.run(User.logout(User.userlogin))  #Пока разлогинимся
            bot.send_message(message.from_user.id, 'Залогинился', parse_mode='Markdown')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
            btn1 = types.KeyboardButton('Домашнее задание')
            btn2 = types.KeyboardButton('Расписание')
            btn3 = types.KeyboardButton('Оценки')
            btn4 = types.KeyboardButton('Разлогинится')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.from_user.id, '❓ Задайте интересующий вас запрос', reply_markup=markup)  # ответ бота
            bot.register_next_step_handler(msg, diaryWork())
        except Exception as exep:
            bot.send_message(message.from_user.id, f'Упс! что-то пошло не так! Код ошибки: {type(exep)}', parse_mode='Markdown')

def diaryWork(message):
        if message.text == '❓ Задайте интересующий вас запрос':
            if message.text == 'Домашнее задание':
                bot.send_message(message.from_user.id, 'Скоро я научусь присылать вам домашнее задание!' + '[Пока перейдите по ссылке в Сетевой город](https://sgo.prim-edu.ru)', parse_mode='Markdown')
            elif message.text == 'Расписание':
                bot.send_message(message.from_user.id, 'Скоро я научусь присылать вам Расписание!' + '[Пока перейдите по ссылке в Сетевой город](https://sgo.prim-edu.ru)', parse_mode='Markdown')
            elif message.text == 'Оценки':
                bot.send_message(message.from_user.id, 'Скоро я научусь присылать вам Оценки! ' + '[Пока перейдите по ссылке в Сетевой город](https://sgo.prim-edu.ru)', parse_mode='Markdown')
            elif message.text == 'Разлогинится':
                try:
                    bot.send_message(message.from_user.id, 'Вы вышли из аккаунта! Спасибо за работу!', parse_mode='Markdown')
                    asyncio.run(User.logout())
                except:
                    bot.send_message(message.from_user.id, 'Упс! что-то пошло не так!', parse_mode='Markdown')

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть_