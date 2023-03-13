#####################################################
#  Этот файл используется для работы над клиентской #
#  частью телеграмм-бота !                          #
#####################################################

import logging  # Библиотека для обработчика событий в виде Логов

from aiogram import types, Dispatcher  # Стандартная библиотека aiogram, использование типов данных и диспетчера событий
from aiogram.dispatcher import FSMContext  # Библиотека aiogram, для работы с автоматом состояний
from aiogram.dispatcher.filters.state import StatesGroup, State  # Библиотека aiogram, для работы с состояниями
from netschoolapi import NetSchoolAPI  # Библиотека для работы с сетевым городом

from create_bot import bot, dp  # Взять из файла create_bot поля bot и dp
from json_work import write_json, read_json  # Взять из файла json_work функции write_json и read_json
from keyboards import keyboards_client_step1, keyboards_client_step2, \
    keyboards_client_step3, keyboards_client_step4  # Импортирование клавиатур из папки с клавиатурами

# функция по обработки логов в консоли
logging.basicConfig(level=logging.INFO)


# Стандартный класс пользователя
class User:
    def __init__(self):
        self.id = 0  # id пользователя
        self.user_login = ''  # Логин
        self.password = ''  # Пароль
        self.school_name = ''  # Название школы
        self.diary = ''  # Последние данные из дневника
        self.url = 'https://region.obramur.ru'  # Ссылка на сайт - она у всех в Амурской области одна


# Класс обработчика машины состояний
class LocalFSM(StatesGroup):
    id_telegram_user = State()  # Шаг 1: Запись id пользователя
    login = State()  # Шаг 2: Запись Логина пользователя
    password = State()  # Шаг 3: Запись Пароля пользователя
    password_conf = State()  # Шаг 4: Запись Подтверждения_Пароля пользователя
    SchoolName = State()  # Шаг 5: Запись Школы пользователя
    auth = State()  # Шаг 6: Авторизация пользователя в системе -> None


# Ограниченный словарь Школ
schools_dict = [
    'МАОУ "Школа № 16 г. Благовещенска"',
    'МАОУ "Школа №26 г. Благовещенска"',
    'МАОУ "Гимназия № 1 г.Благовещенска"',
    'МАОУ "Школа №28 г. Благовещенска"',
    'МАОУ "Школа №27 города Благовещенска"',
    'МАОУ "Школа № 14 г. Благовещенска"'
]


# Функция начала работы бота
async def start(message: types.Message):  # Работает по команде /start
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgEAAxkBAAEIEiBkCqVNHsCtXOfYvGEfsy0Hh6wdbQAC-AEAAjgOghFb9OZ62rUyZC8E')
    await message.answer("👋 Привет! Я твой бот-помошник в сетевом городе!", reply_markup=keyboards_client_step1)
    await message.answer("Я могу присылать тебе:\n - 🗓*текущее расписание*,\n - 📚*домашнее задание*,"
                         "\n - 💯*оценки по предметам*", parse_mode='Markdown')


# Функция начала работы бота
async def help_pls(message: types.Message):  # Работает по команде /help
    pass
    # Тут мне нужно написать что будет выдавать бот при команде помощи
    # Предположительно нужно вывести стикер и сообщение об полном описание бота! Сделать!!!!


# Функция для отлова пользовательских сообщений
async def get_text_messages(message: types.Message, state: FSMContext):  # Работает при любом перечисленном сообщение
    # -----------------------------------------------------------------------------
    if message.text == '👋 Поздороваться':  # При вводе 👋 Поздороваться будет ->
        await bot.send_sticker(message.from_user.id,
                               sticker='CAACAgEAAxkBAAEIEhxkCqUsNWrPJxHbGi1p_1-F7CY8LQAC7QEAAjgOghE8J4BsgBeaAy8E')
        await message.answer('И тебе привет! 🐶\n⌛️ Хватит терять время! \n Чтобы получить'
                             ' данные, сначала *авторизуйся!*🔓', reply_markup=keyboards_client_step2,
                             parse_mode='Markdown')
    # -----------------------------------------------------------------------------
    elif message.text == '🔓 Авторизоваться':  # При вводе 🔓 Авторизоваться будет ->
        user_exist = read_json("data/data.json")
        if message.from_user.id != user_exist['id']:  # Проверка авторизован пользователь ранее или нет (если нет)
            await message.answer('Отлично! Осталось дело за малым! 👍\n'
                                 '- Пожалуйста введите - 👤*Логин* для входа в сетевой город.\n'
                                 '- *Например*: ИвановВ1', parse_mode='Markdown')
            await message.answer('\- *Подсказка*: ||Обычно его вам выдают в школе||', parse_mode='Markdownv2')
            await state.set_state(LocalFSM.login.state)
        else:  # Проверка авторизован пользователь ранее или нет (если да)
            await message.answer('Вы уже авторизовывались ранее! Переводим вас в рабочий режим! 💪')
            await state.set_state(LocalFSM.auth.state)
    # -----------------------------------------------------------------------------
    elif message.text == '📚 Домашнее задание':  # При вводе 📚 Домашнее задание будет ->
        await message.answer(f'Скоро я научусь присылать вам домашнее задание!',
                             reply_markup=keyboards_client_step3, parse_mode='Markdown')
        # Тут идёт блок кода для работы с домашним заданием - его я добавлю позднее
    # -----------------------------------------------------------------------------
    elif message.text == '🕒 Расписание':  # При вводе 🕒 Расписание будет ->
        await message.answer(f'Скоро я научусь присылать вам Расписание!',
                             reply_markup=keyboards_client_step3, parse_mode='Markdown')
        # Тут идёт блок кода для работы с расписанием - его я добавлю позднее
    # -----------------------------------------------------------------------------
    elif message.text == '💯 Оценки':  # При вводе 💯 Оценки будет ->
        await message.answer(f'Скоро я научусь присылать вам Оценки!',
                             reply_markup=keyboards_client_step3, parse_mode='Markdown')
        # Тут идёт блок кода для работы с оценками - его я добавлю позднее
    # -----------------------------------------------------------------------------
    elif message.text == '🚪 Разлогинится':  # При вводе 🚪 Разлогинится будет ->
        try:  # Встроенная функция поиска исключения
            user = User()  # Создание экземпляра класса Пользователя
            connection = NetSchoolAPI(user.url)  # Реализация подключения к сетевому городу
            await connection.logout()  # Реализация отключения от сетевого города
            await bot.send_sticker(message.from_user.id,
                                   sticker='CAACAgEAAxkBAAEIG0JkDfSK95D5Ud2CEm1i5T4zQLzIJgAC5QEAAjgOghGurgLq55jGpC8E')
            await message.answer('Вы *вышли* из аккаунта!🚪 \n *Спасибо за работу!*',
                                 reply_markup=keyboards_client_step1,
                                 parse_mode='Markdown')
        except Exception as e:  # Если исключение с ошибкой случилось ->
            await bot.send_sticker(message.from_user.id,
                                   sticker='CAACAgEAAxkBAAEIG0RkDfS4-XLEyIEaFQceYrzNsXrKMgAC-QEAAjgOghHcO4dxtT-qti8E')
            await message.answer(f'Упс! что-то пошло не так! Код ошибки: {type(e)}', parse_mode='Markdown')


# Функция-состояние для получения логина пользователя
async def state_login(message: types.Message, state: FSMContext):  # Переходит сюда после кнопки Авторизоваться
    async with state.proxy() as data:
        data['id_telegram_user'] = message.from_user.id  # Хранение id пользователя Телеграмм
        data['login'] = message.text  # Хранение Логина пользователя Сетевым городом
    await message.reply(f'Введенный вами 👤логин: {message.text}')
    await message.answer(f'🔑Введитие ваш *пароль* от кабинета сетевого города!\n'
                         f'--------------------------------------------------\n'
                         f'‼️Обращаю ваше внимание, если вы забыли пароль - его можно'
                         f'восстановить только из *веб-интерфейса* или *мобильного приложения* Сетевой город!',
                         parse_mode='Markdown')
    await LocalFSM.next()  # Следующий шаг по обработчику событий -> Пароль


# Функция-состояние для получения пароля пользователя
async def state_password(message: types.Message, state: FSMContext):  # Переходит сюда после Ввода логина
    async with state.proxy() as data:
        data['password'] = message.text  # Хранение Пароля пользователя Сетевым городом
    await message.reply(f'Введенный вами 🔑пароль: ||{message.text}||', parse_mode="markdownv2")
    await message.answer(f'Введите 🔑пароль ещё раз для *подтверждения!*', parse_mode="Markdown")
    await LocalFSM.next()  # Следующий шаг по обработчику событий -> Подтверждение_Пароля


# Функция-состояние для получения подтверждения пароля пользователя
async def state_password_conf(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password_conf'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
    if data['password'] == data['password_conf']:  # Сравнение пароля и пароля подтверждения
        await message.reply(f'Введенное вами 🔑подтверждение: ||{message.text}||', parse_mode="markdownv2")
        await message.answer(f'Пароли совпадают!\n'
                             f'--------------------------------------------------\n'
                             f'теперь пожалуйста выберите вашу 🏫*школу* из списка!',
                             reply_markup=keyboards_client_step4, parse_mode="Markdown")
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    else:  # Если пароли не совпали
        await bot.send_sticker(message.from_user.id,
                               sticker='CAACAgEAAxkBAAEIG0ZkDfY7MW3rRPfOfAZyqgvIxgprkgAC8gEAAjgOghFkeRhU3RO6Bi8E')
        await message.answer(f'❗️ Возникла ошибка! \n'
                             f'🔑Пароли не совпадают - пожалуйста, введите ещё раз свой *основной пароль*!',
                             parse_mode='Markdown')
        await state.set_state(LocalFSM.password.state)  # Возврат к предыдущему шагу <- Пароль


# Функция-состояние с Обратным вызовом - для выбора школы из списка
@dp.callback_query_handler(text_contains="School_", state=LocalFSM.SchoolName)
async def state_school_name(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data_json = {  # Создаем словарик данных пользователя
            'id': int(data['id_telegram_user']),
            'user_login': str(data['login']),
            'password': str(data['password']),
            'school_name': schools_dict[int(callback.data.replace('School_', ''))],
            'diary': None
        }
    write_json(data_json, "data/data.json")  # Записываем словарик в файл данных data.json
    print(read_json("data/data.json"))  # Проверка - выводим в консоль данные из файла data.json
    await callback.message.reply(f"Выбранная вами 🏫школа: {schools_dict[int(callback.data.replace('School_', ''))]}")
    await callback.message.answer(
        f'🌐Введите любой символ если вы согласны с '
        f'<a href="https://www.consultant.ru/document/cons_doc_LAW_61801/315f051396c88f1e4f827ba3f2ae313d999a1873/"><b>'
        f'условиями обработки данных</b></a>! Или покиньте бот',
        parse_mode='html')
    await state.set_state(LocalFSM.auth.state)  # Следующий шаг по обработчику событий -> авторизация


# Функция-состояние для авторизации пользователя в Сетевом городе
async def state_auth(message: types.Message, state: FSMContext):
    try:  # Выполняется отлов ошибок при авторизации
        json_data = read_json("data/data.json")  # Получаем данные из файла
        user = User()  # Создаём экземпляр класса
        user.user_login = json_data['user_login']  # Записываем данные в класс Пользователь из файла
        user.password = json_data['password']
        user.school_name = json_data['school_name']
        connection = NetSchoolAPI(user.url)  # Создаем подключение
        await connection.login(user.user_login, user.password, user.school_name)  # Логинимся
        await bot.send_sticker(message.from_user.id,
                               sticker='CAACAgEAAxkBAAEIEhRkCqJbO7paRvBXqoEqNJHqfkPMwQACLgEAAmlAwUU75COP0TwvfC8E')
        await message.answer(f'Спасибо! Мы запомнили ваши данные, чтобы больше не нужно было ничего вводить!')
        await message.answer('Залогинился! ❓ Задайте интересующий вас запрос', reply_markup=keyboards_client_step3)
        await state.finish()  # Завершаем шаг
    except Exception as e:  # Если ошибка при авторизации случилась
        print(type(e))
        if str(type(e)) == "<class 'netschoolapi.errors.SchoolNotFoundError'>":  # Ошибка неправильно введенной Школы
            await bot.send_sticker(message.from_user.id,
                                   sticker='CAACAgEAAxkBAAEIG0RkDfS4-XLEyIEaFQceYrzNsXrKMgAC-QEAAjgOghHcO4dxtT-qti8E')
            await message.answer(f'*Упс!* что-то пошло не так! Вы неверно ввели *школу*!',
                                 reply_markup=types.ReplyKeyboardRemove(),
                                 parse_mode='Markdown')
            await message.answer(f'Введите 🏫*школу* ещё раз и мы попробуем вас авторизовать!',
                                 reply_markup=keyboards_client_step4,
                                 parse_mode='Markdown')
            await state.set_state(LocalFSM.SchoolName.state)  # Переходим на шаг <- Ввода школы
        elif str(
                type(
                    e)) == "<class 'netschoolapi.errors.AuthError'>":  # Ошибка неправильно введенного Логина или пароля
            await bot.send_sticker(message.from_user.id,
                                   sticker='CAACAgEAAxkBAAEIG0RkDfS4-XLEyIEaFQceYrzNsXrKMgAC-QEAAjgOghHcO4dxtT-qti8E')
            await message.answer(f'*Упс!* что-то пошло не так! \nВы неверно ввели *логин или пароль*!'
                                 f'Введите 👤*логин* и 🔑*пароль* ещё раз - и мы попробуем вас авторизовать'
                                 f'\n------------------------------------------------------------------------'
                                 f'Напоминаем, первым вводится 👤*логин*!',
                                 reply_markup=types.ReplyKeyboardRemove(),
                                 parse_mode='Markdown')
            await state.set_state(LocalFSM.login.state)  # Переходим на шаг <- Ввода логина
        else:  # Если сервис баз данных недоступен
            await bot.send_sticker(message.from_user.id,
                                   sticker='CAACAgEAAxkBAAEIG0RkDfS4-XLEyIEaFQceYrzNsXrKMgAC-QEAAjgOghHcO4dxtT-qti8E')
            await bot.send_message(message.from_user.id,
                                   f'*Упс!* что-то пошло не так! Сервис сейчас недоступен. Попробуйте войти '
                                   f'позже. Код ошибки: {type(e)}',
                                   reply_markup=keyboards_client_step2, parse_mode='Markdown')
            await state.finish()  # Завершаем шаг


# Функция регистрации диспетчеров-обработчиков в системе - чтобы не писать каждый обработчик в шапке
def registration_handler_client(disp: Dispatcher):
    disp.register_message_handler(start, commands=['start'])
    disp.register_message_handler(help_pls, commands=['help'])
    disp.register_message_handler(get_text_messages, content_types=['text'], state=None)
    disp.register_message_handler(state_login, state=LocalFSM.login)
    disp.register_message_handler(state_password, state=LocalFSM.password)
    disp.register_message_handler(state_password_conf, state=LocalFSM.password_conf)
    disp.register_message_handler(state_auth, state=LocalFSM.auth)
