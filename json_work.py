######################################
#  Этот файл используется для работы #
#  с библиотекой Json!               #
######################################
import json


# Функция для записи данных в файл data.json и last_response
def write_json(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, indent=4)  # Пример работы writeJson(user_data2,'data/data.json')


# Функция для чтения данных из файлов data.json и last_response
def read_json(filename):
    with open(filename, "r", encoding='utf-8') as read_file:  # Пример data['user_data2'].append(User().__dict__)
        return json.load(read_file)  # Пример работы readJson('data/data.json')
