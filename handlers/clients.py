#####################################################
#  Этот файл используется для работы над клиентской #
#  частью телеграмм-бота !                          #
#####################################################

import logging  # Библиотека для обработчика событий в виде Логов
from datetime import date, timedelta

from aiogram import types, Dispatcher  # Стандартная библиотека aiogram, использование типов данных и диспетчера событий
from aiogram.dispatcher import FSMContext  # Библиотека aiogram, для работы с автоматом состояний
from aiogram.dispatcher.filters.state import StatesGroup, State  # Библиотека aiogram, для работы с состояниями
from netschoolapi import NetSchoolAPI  # Библиотека для работы с сетевым городом

from create_bot import bot, dp  # Взять из файла create_bot поля bot и dp
from json_work import write_json, read_json  # Взять из файла json_work функции write_json и read_json
from keyboards import keyboards_client_step1, keyboards_client_step2, \
    keyboards_client_step3, keyboards_client_step4, keyboards_client_step5, \
    keyboards_client_step6, keyboards_client_step7, keyboards_client_step8, \
    keyboards_client_step9, keyboards_client_step10, \
    keyboards_client_step11  # Импортирование клавиатур из папки с клавиатурами

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
    timetable_week = State()
    timetable_day = State()
    homework_week = State()
    homework_day = State()
    mark_week = State()
    mark_day = State()


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
    await message.answer("👋 Привет! Я твой бот-помощник в сетевом городе!", reply_markup=keyboards_client_step1)
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
            await message.answer('Вы уже авторизовывались ранее! Переводим вас в рабочий режим! 💪',
                                 reply_markup=keyboards_client_step7)
            await state.set_state(LocalFSM.auth.state)
    # -----------------------------------------------------------------------------
    elif message.text == '📚 Домашнее задание':  # При вводе 📚 Домашнее задание будет ->
        await message.answer(
            f'Текущая дата на сегодня: {date.today()} \n Выберите действие для вывода домашнего задания!',
            reply_markup=keyboards_client_step8, parse_mode='Markdown')
        await state.set_state(LocalFSM.homework_week.state)
    # -----------------------------------------------------------------------------
    elif message.text == '🕒 Расписание':  # При вводе 🕒 Расписание будет ->
        await message.answer(f'Текущая дата на сегодня: {date.today()} \n Выберите действие для вывода расписания!',
                             reply_markup=keyboards_client_step5, parse_mode='Markdown')
        await state.set_state(LocalFSM.timetable_week.state)
    # -----------------------------------------------------------------------------
    elif message.text == '💯 Оценки':  # При вводе 💯 Оценки будет ->
        await message.answer(
            f'Текущая дата на сегодня: {date.today()} \n Выберите действие для вывода Оценок!',
            reply_markup=keyboards_client_step10, parse_mode='Markdown')
        await state.set_state(LocalFSM.mark_week.state)
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


async def diary_timetable_week(message: types.Message, state: FSMContext):
    if message.text == '🔙 Вернуться':
        await message.answer(f'Выход в главное меню', reply_markup=keyboards_client_step3, parse_mode='Markdown')
        await state.finish()
    elif message.text == '⬅️ Предыдущая':
        await message.answer(f'Неделя: {date.today() - timedelta(days=7)}-{date.today()}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step6, parse_mode='Markdown')
        async with state.proxy() as data:
            data['timetable_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == 'Текущая неделя':
        await message.answer(f'Неделя: {date.today()}-{date.today() + timedelta(days=7)}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step6, parse_mode='Markdown')
        async with state.proxy() as data:
            data['timetable_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == 'Следующая ➡️':
        await message.answer(f'Неделя: {date.today() + timedelta(days=7)}-{date.today() + timedelta(days=14)}',
                             parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step6, parse_mode='Markdown')
        async with state.proxy() as data:
            data['timetable_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы


async def diary_timetable_day(message: types.Message, state: FSMContext):
    json_data = read_json("data/data.json")  # Получаем данные из файла
    user = User()  # Создаём экземпляр класса
    user.user_login = json_data['user_login']  # Записываем данные в класс Пользователь из файла
    user.password = json_data['password']
    user.school_name = json_data['school_name']
    connection = NetSchoolAPI(user.url)
    await connection.login(user.user_login, user.password, user.school_name)  # Логинимся
    current_date = date.today()
    if current_date.weekday() != 0:
        current_date = current_date - timedelta(days=current_date.weekday())

    async with state.proxy() as data:
        if data['timetable_week'] == "⬅️ Предыдущая":
            week_start = current_date - timedelta(days=7)
            week_end = current_date
            current_diary = await connection.diary(week_start, week_end)
        if data['timetable_week'] == "Текущая неделя":
            current_diary = await connection.diary()
        if data['timetable_week'] == "Следующая ➡️":
            week_start = current_date + timedelta(days=7)
            week_end = current_date + timedelta(days=14)
            current_diary = await connection.diary(week_start, week_end)
    if len(current_diary.schedule[0].lessons) > 2:
        week = {
            'monday': current_diary.schedule[0],
            'tuesday': current_diary.schedule[1],
            'wednesday': current_diary.schedule[2],
            'thursday': current_diary.schedule[3],
            'friday': current_diary.schedule[4],
            'saturday': current_diary.schedule[5]
        }
        # Правка массива если у него есть -1 урок
        for i in range(len(week['monday'].lessons)):
            if week['monday'].lessons[i].number == -1:
                week['monday'].lessons.insert(0, week['monday'].lessons[i])
                week['monday'].lessons.pop(i + 1)

        for i in range(len(week['tuesday'].lessons)):
            if week['tuesday'].lessons[i].number == -1:
                week['tuesday'].lessons.insert(0, week['tuesday'].lessons[i])
                week['tuesday'].lessons.pop(i + 1)

        for i in range(len(week['wednesday'].lessons)):
            if week['wednesday'].lessons[i].number == -1:
                week['wednesday'].lessons.insert(0, week['wednesday'].lessons[i])
                week['wednesday'].lessons.pop(i + 1)

        for i in range(len(week['thursday'].lessons)):
            if week['thursday'].lessons[i].number == -1:
                week['thursday'].lessons.insert(0, week['thursday'].lessons[i])
                week['thursday'].lessons.pop(i + 1)

        for i in range(len(week['friday'].lessons)):
            if week['friday'].lessons[i].number == -1:
                week['friday'].lessons.insert(0, week['friday'].lessons[i])
                week['friday'].lessons.pop(i + 1)

        for i in range(len(week['saturday'].lessons)):
            if week['saturday'].lessons[i].number == -1:
                week['saturday'].lessons.insert(0, week['saturday'].lessons[i])
                week['saturday'].lessons.pop(i + 1)

    else:
        current_diary.schedule = 'Каникулы'
        week = {
            'monday': current_diary.schedule,
            'tuesday': current_diary.schedule,
            'wednesday': current_diary.schedule,
            'thursday': current_diary.schedule,
            'friday': current_diary.schedule,
            'saturday': current_diary.schedule
        }

    if message.text == '🔙.':
        await message.answer(f'Вышел к неделям',
                             reply_markup=keyboards_client_step5, parse_mode='Markdown')
        await LocalFSM.previous()
    elif message.text == 'ПН':
        await message.answer(f'Расписание на понедельник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['monday'].lessons)
            for i in range(len(week['monday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["monday"].lessons[i].start.strftime("%H:%M")}-{week["monday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["monday"].lessons[i].room}', reply_markup=keyboards_client_step6)
    elif message.text == 'ВТ':
        await message.answer(f'Расписание на вторник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['tuesday'].lessons)
            for i in range(len(week['tuesday'].lessons)):
                await message.answer(
                    f'{str(week["tuesday"].lessons[i].number).rjust(2, " ")}. {week["tuesday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["tuesday"].lessons[i].start.strftime("%H:%M")}-{week["tuesday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["tuesday"].lessons[i].room}', reply_markup=keyboards_client_step6)
    elif message.text == 'СР':
        await message.answer(f'Расписание на среду:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['wednesday'].lessons)
            for i in range(len(week['wednesday'].lessons)):
                await message.answer(
                    f'{str(week["wednesday"].lessons[i].number).rjust(2, " ")}. {week["wednesday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["wednesday"].lessons[i].start.strftime("%H:%M")}-{week["wednesday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["wednesday"].lessons[i].room}', reply_markup=keyboards_client_step6)
    elif message.text == 'ЧТ':
        await message.answer(f'Расписание на четверг:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['thursday'].lessons)
            for i in range(len(week['thursday'].lessons)):
                await message.answer(
                    f'{str(week["thursday"].lessons[i].number).rjust(2, " ")}. {week["thursday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["thursday"].lessons[i].start.strftime("%H:%M")}-{week["thursday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["thursday"].lessons[i].room}', reply_markup=keyboards_client_step6)
    elif message.text == 'ПТ':
        await message.answer(f'Расписание на пятницу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['friday'].lessons)
            for i in range(len(week['friday'].lessons)):
                await message.answer(
                    f'{str(week["friday"].lessons[i].number).rjust(2, " ")}. {week["friday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["friday"].lessons[i].start.strftime("%H:%M")}-{week["friday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["friday"].lessons[i].room}', reply_markup=keyboards_client_step6)
    elif message.text == 'СБ':
        await message.answer(f'Расписание на субботу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step6)
        else:
            print(week['saturday'].lessons)
            for i in range(len(week['saturday'].lessons)):
                await message.answer(
                    f'{str(week["saturday"].lessons[i].number).rjust(2, " ")}. {week["saturday"].lessons[i].subject.ljust(17, " ")}'
                    f' | {week["saturday"].lessons[i].start.strftime("%H:%M")}-{week["saturday"].lessons[i].end.strftime("%H:%M")}'
                    f' | {week["saturday"].lessons[i].room}', reply_markup=keyboards_client_step6)


async def diary_homework_week(message: types.Message, state: FSMContext):
    if message.text == '.🔙 Вернуться':
        await message.answer(f'Выход в главное меню', reply_markup=keyboards_client_step3, parse_mode='Markdown')
        await state.finish()
    elif message.text == '.⬅️ Предыдущая':
        await message.answer(f'Неделя: {date.today() - timedelta(days=7)}-{date.today()}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step9, parse_mode='Markdown')
        async with state.proxy() as data:
            data['homework_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == '.Текущая неделя':
        await message.answer(f'Неделя: {date.today()}-{date.today() + timedelta(days=7)}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step9, parse_mode='Markdown')
        async with state.proxy() as data:
            data['homework_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == '.Следующая ➡️':
        await message.answer(f'Неделя: {date.today() + timedelta(days=7)}-{date.today() + timedelta(days=14)}',
                             parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step9, parse_mode='Markdown')
        async with state.proxy() as data:
            data['homework_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы


async def diary_homework_day(message: types.Message, state: FSMContext):
    json_data = read_json("data/data.json")  # Получаем данные из файла
    user = User()  # Создаём экземпляр класса
    user.user_login = json_data['user_login']  # Записываем данные в класс Пользователь из файла
    user.password = json_data['password']
    user.school_name = json_data['school_name']
    connection = NetSchoolAPI(user.url)
    await connection.login(user.user_login, user.password, user.school_name)  # Логинимся
    current_date = date.today()
    if current_date.weekday() != 0:
        current_date = current_date - timedelta(days=current_date.weekday())

    async with state.proxy() as data:
        if data['homework_week'] == ".⬅️ Предыдущая":
            week_start = current_date - timedelta(days=7)
            week_end = current_date
            current_diary = await connection.diary(week_start, week_end)
        if data['homework_week'] == ".Текущая неделя":
            current_diary = await connection.diary()
        if data['homework_week'] == ".Следующая ➡️":
            week_start = current_date + timedelta(days=7)
            week_end = current_date + timedelta(days=14)
            current_diary = await connection.diary(week_start, week_end)
    if len(current_diary.schedule[0].lessons) > 2:
        week = {
            'monday': current_diary.schedule[0],
            'tuesday': current_diary.schedule[1],
            'wednesday': current_diary.schedule[2],
            'thursday': current_diary.schedule[3],
            'friday': current_diary.schedule[4],
            'saturday': current_diary.schedule[5]
        }
        # Правка массива если у него есть -1 урок
        for i in range(len(week['monday'].lessons)):
            if week['monday'].lessons[i].number == -1:
                week['monday'].lessons.insert(0, week['monday'].lessons[i])
                week['monday'].lessons.pop(i + 1)

        for i in range(len(week['tuesday'].lessons)):
            if week['tuesday'].lessons[i].number == -1:
                week['tuesday'].lessons.insert(0, week['tuesday'].lessons[i])
                week['tuesday'].lessons.pop(i + 1)

        for i in range(len(week['wednesday'].lessons)):
            if week['wednesday'].lessons[i].number == -1:
                week['wednesday'].lessons.insert(0, week['wednesday'].lessons[i])
                week['wednesday'].lessons.pop(i + 1)

        for i in range(len(week['thursday'].lessons)):
            if week['thursday'].lessons[i].number == -1:
                week['thursday'].lessons.insert(0, week['thursday'].lessons[i])
                week['thursday'].lessons.pop(i + 1)

        for i in range(len(week['friday'].lessons)):
            if week['friday'].lessons[i].number == -1:
                week['friday'].lessons.insert(0, week['friday'].lessons[i])
                week['friday'].lessons.pop(i + 1)

        for i in range(len(week['saturday'].lessons)):
            if week['saturday'].lessons[i].number == -1:
                week['saturday'].lessons.insert(0, week['saturday'].lessons[i])
                week['saturday'].lessons.pop(i + 1)

    else:
        current_diary.schedule = 'Каникулы'
        week = {
            'monday': current_diary.schedule,
            'tuesday': current_diary.schedule,
            'wednesday': current_diary.schedule,
            'thursday': current_diary.schedule,
            'friday': current_diary.schedule,
            'saturday': current_diary.schedule
        }

    if message.text == '.🔙.':
        await message.answer(f'Вышел к неделям',
                             reply_markup=keyboards_client_step8, parse_mode='Markdown')
        await LocalFSM.previous()
    elif message.text == '.ПН':
        await message.answer(f'Домашнее задание на понедельник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            for i in range(len(week['monday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)
    elif message.text == '.ВТ':
        await message.answer(f'Домашнее задание вторник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            print(week['tuesday'].lessons)
            for i in range(len(week['tuesday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)
    elif message.text == '.СР':
        await message.answer(f'Домашнее задание на среду:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            print(week['wednesday'].lessons)
            for i in range(len(week['wednesday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)
    elif message.text == '.ЧТ':
        await message.answer(f'Домашнее задание на четверг:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            print(week['thursday'].lessons)
            for i in range(len(week['thursday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)
    elif message.text == '.ПТ':
        await message.answer(f'Домашнее задание на пятницу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            print(week['friday'].lessons)
            for i in range(len(week['friday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)
    elif message.text == '.СБ':
        await message.answer(f'Домашнее задание на субботу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step9)
        else:
            print(week['saturday'].lessons)
            for i in range(len(week['saturday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].content}', reply_markup=keyboards_client_step9)


async def diary_marks_week(message: types.Message, state: FSMContext):
    if message.text == '.🔙 Вернуться.':
        await message.answer(f'Выход в главное меню', reply_markup=keyboards_client_step3, parse_mode='Markdown')
        await state.finish()
    elif message.text == '.⬅️ Предыдущая.':
        await message.answer(f'Неделя: {date.today() - timedelta(days=7)}-{date.today()}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step11, parse_mode='Markdown')
        async with state.proxy() as data:
            data['mark_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == '.Текущая неделя.':
        await message.answer(f'Неделя: {date.today()}-{date.today() + timedelta(days=7)}', parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step11, parse_mode='Markdown')
        async with state.proxy() as data:
            data['mark_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы
    elif message.text == '.Следующая ➡️.':
        await message.answer(f'Неделя: {date.today() + timedelta(days=7)}-{date.today() + timedelta(days=14)}',
                             parse_mode='Markdown')
        await message.answer(f'Выберите день недели!', reply_markup=keyboards_client_step11, parse_mode='Markdown')
        async with state.proxy() as data:
            data['mark_week'] = message.text  # Хранение Подтверждения пароля пользователя Сетевым городом
        await LocalFSM.next()  # Следующий шаг по обработчику событий -> Выбор школы


async def diary_marks_day(message: types.Message, state: FSMContext):
    json_data = read_json("data/data.json")  # Получаем данные из файла
    user = User()  # Создаём экземпляр класса
    user.user_login = json_data['user_login']  # Записываем данные в класс Пользователь из файла
    user.password = json_data['password']
    user.school_name = json_data['school_name']
    connection = NetSchoolAPI(user.url)
    await connection.login(user.user_login, user.password, user.school_name)  # Логинимся
    current_date = date.today()
    if current_date.weekday() != 0:
        current_date = current_date - timedelta(days=current_date.weekday())

    async with state.proxy() as data:
        if data['mark_week'] == ".⬅️ Предыдущая.":
            week_start = current_date - timedelta(days=7)
            week_end = current_date
            current_diary = await connection.diary(week_start, week_end)
        if data['mark_week'] == ".Текущая неделя.":
            current_diary = await connection.diary()
        if data['mark_week'] == ".Следующая ➡️.":
            week_start = current_date + timedelta(days=7)
            week_end = current_date + timedelta(days=14)
            current_diary = await connection.diary(week_start, week_end)
    if len(current_diary.schedule[0].lessons) > 2:
        week = {
            'monday': current_diary.schedule[0],
            'tuesday': current_diary.schedule[1],
            'wednesday': current_diary.schedule[2],
            'thursday': current_diary.schedule[3],
            'friday': current_diary.schedule[4],
            'saturday': current_diary.schedule[5]
        }
        # Правка массива если у него есть -1 урок
        for i in range(len(week['monday'].lessons)):
            if week['monday'].lessons[i].number == -1:
                week['monday'].lessons.insert(0, week['monday'].lessons[i])
                week['monday'].lessons.pop(i + 1)

        for i in range(len(week['tuesday'].lessons)):
            if week['tuesday'].lessons[i].number == -1:
                week['tuesday'].lessons.insert(0, week['tuesday'].lessons[i])
                week['tuesday'].lessons.pop(i + 1)

        for i in range(len(week['wednesday'].lessons)):
            if week['wednesday'].lessons[i].number == -1:
                week['wednesday'].lessons.insert(0, week['wednesday'].lessons[i])
                week['wednesday'].lessons.pop(i + 1)

        for i in range(len(week['thursday'].lessons)):
            if week['thursday'].lessons[i].number == -1:
                week['thursday'].lessons.insert(0, week['thursday'].lessons[i])
                week['thursday'].lessons.pop(i + 1)

        for i in range(len(week['friday'].lessons)):
            if week['friday'].lessons[i].number == -1:
                week['friday'].lessons.insert(0, week['friday'].lessons[i])
                week['friday'].lessons.pop(i + 1)

        for i in range(len(week['saturday'].lessons)):
            if week['saturday'].lessons[i].number == -1:
                week['saturday'].lessons.insert(0, week['saturday'].lessons[i])
                week['saturday'].lessons.pop(i + 1)

    else:
        current_diary.schedule = 'Каникулы'
        week = {
            'monday': current_diary.schedule,
            'tuesday': current_diary.schedule,
            'wednesday': current_diary.schedule,
            'thursday': current_diary.schedule,
            'friday': current_diary.schedule,
            'saturday': current_diary.schedule
        }

    if message.text == '🔙..':
        await message.answer(f'Вышел к неделям',
                             reply_markup=keyboards_client_step10, parse_mode='Markdown')
        await LocalFSM.previous()
    elif message.text == '.ПН.':
        await message.answer(f'Оценка за понедельник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            for i in range(len(week['monday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)
    elif message.text == '.ВТ.':
        await message.answer(f'Оценка за вторник:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            print(week['tuesday'].lessons)
            for i in range(len(week['tuesday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)
    elif message.text == '.СР.':
        await message.answer(f'Оценка за среду:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            print(week['wednesday'].lessons)
            for i in range(len(week['wednesday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)
    elif message.text == '.ЧТ.':
        await message.answer(f'Оценка за четверг:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            print(week['thursday'].lessons)
            for i in range(len(week['thursday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)
    elif message.text == '.ПТ.':
        await message.answer(f'Оценка за пятницу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            print(week['friday'].lessons)
            for i in range(len(week['friday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)
    elif message.text == '.СБ.':
        await message.answer(f'Оценка за субботу:', parse_mode='Markdown')
        if week['monday'] == 'Каникулы':
            await message.answer("Каникулы", reply_markup=keyboards_client_step11)
        else:
            print(week['saturday'].lessons)
            for i in range(len(week['saturday'].lessons)):
                await message.answer(
                    f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
                    f' \n {week["monday"].lessons[i].assignments[0].mark}', reply_markup=keyboards_client_step11)


# Функция регистрации диспетчеров-обработчиков в системе - чтобы не писать каждый обработчик в шапке
def registration_handler_client(disp: Dispatcher):
    disp.register_message_handler(start, commands=['start'])
    disp.register_message_handler(help_pls, commands=['help'])
    disp.register_message_handler(get_text_messages, content_types=['text'], state=None)
    disp.register_message_handler(state_login, state=LocalFSM.login)
    disp.register_message_handler(state_password, state=LocalFSM.password)
    disp.register_message_handler(state_password_conf, state=LocalFSM.password_conf)
    disp.register_message_handler(state_auth, state=LocalFSM.auth)
    disp.register_message_handler(diary_timetable_week, content_types=['text'], state=LocalFSM.timetable_week)
    disp.register_message_handler(diary_timetable_day, content_types=['text'], state=LocalFSM.timetable_day)
    disp.register_message_handler(diary_homework_week, content_types=['text'], state=LocalFSM.homework_week)
    disp.register_message_handler(diary_homework_day, content_types=['text'], state=LocalFSM.homework_day)
    disp.register_message_handler(diary_marks_week, content_types=['text'], state=LocalFSM.mark_week)
    disp.register_message_handler(diary_marks_day, content_types=['text'], state=LocalFSM.mark_day)
