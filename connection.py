####################################################
#  Это файл для работы с подключением к NetSchool! #
#  Тут происходит авторизация и обработка данных!  #
####################################################

from netschoolapi import NetSchoolAPI


# Подключение к сетевому городу
async def login(userlogin, password, schoolname):
    ns = NetSchoolAPI(
        'https://region.obramur.ru')  # Создаём клиент. Через него мы будем обращаться к АПИ электронного дневника
    await ns.login(userlogin, password, schoolname)  # Логинимся


# Разлогиним телеграмм бота
async def logout():
    ns = NetSchoolAPI(
        'https://region.obramur.ru')  # Создаём клиент. Через него мы будем обращаться к АПИ электронного дневника
    await ns.logout()  # Разлогиниться - обязательно!


async def diary():
    ns = NetSchoolAPI(
        'https://region.obramur.ru')  # Создаём клиент. Через него мы будем обращаться к АПИ электронного дневника
    diary = await ns.diary()  # Запрашиваем дневник
    return diary

# Пример работы с АПИ
# async def main():
#     ns = NetSchoolAPI('https://region.obramur.ru')
#
#     await ns.login(
#         'Login',  # Логин
#         'Password',  # Пароль
#         'SchoolName',  # Название школы
#     )
#
#     # Работа с расписанием
#     CurrentWeekDiary = await ns.diary(date(2023, 2, 13), date(2023, 2, 18))
#     LastWeekDiary = await ns.diary(CurrentWeekDiary.start - timedelta(days=7), CurrentWeekDiary.end - timedelta(days=7))
#     NextWeekDiary = await ns.diary(CurrentWeekDiary.start + timedelta(days=7), CurrentWeekDiary.end + timedelta(days=7))
#
#     week = {
#         'monday': CurrentWeekDiary.schedule[0],
#         'tuesday': CurrentWeekDiary.schedule[1],
#         'wednesday': CurrentWeekDiary.schedule[2],
#         'thursday': CurrentWeekDiary.schedule[3],
#         'friday': CurrentWeekDiary.schedule[4],
#         'saturday': CurrentWeekDiary.schedule[5]
#     }
#
#     # Правка массива если у него есть -1 урок
#     for i in range(len(week['monday'].lessons)):
#         if week['monday'].lessons[i].number == -1:
#             week['monday'].lessons.insert(0, week['monday'].lessons[i])
#             week['monday'].lessons.pop(i + 1)
#
#     print(f'Ваше текущее расписание: с {CurrentWeekDiary.start} по {CurrentWeekDiary.end}\n'
#           f'Понедельник:')
#
#     for i in range(len(week['monday'].lessons)):
#         print(
#             f'{str(week["monday"].lessons[i].number).rjust(2, " ")}. {week["monday"].lessons[i].subject.ljust(17, " ")}'
#             f' | {week["monday"].lessons[i].start.strftime("%H:%M")}-{week["monday"].lessons[i].end.strftime("%H:%M")}'
#             f' | {week["monday"].lessons[i].room}')
#
#     await ns.logout()
#
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())
