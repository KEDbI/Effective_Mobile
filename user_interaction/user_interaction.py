from pathlib import Path
from txt_database.txt_database import Library
from sqlite_database.sqlite_database import SqliteDatabase


def start() -> Library | SqliteDatabase | None:
    """Функция выводит пользователю приветствие, а также запрашивает желаемый тип бд. Возвращает объект бд или None,
    если пользователь ввел 'exit' """

    greetings = ('\nДобрый день! Вы зашли в систему управления библиотекой книг. Для начала работы выберите тип бд: \n'
                 '1: 1 или txt - текстовый файл library.txt \n'
                 '2: 2 или sqlite - реляционная база данных sqlite \n'
                 '3: 3 или exit - выход из программы')
    print(greetings)

    # запрос желаемой бд
    while True:
        db = input('Введите желаемую бд: ')
        if db == '1' or db.lower() == 'txt':
            db = Library(Path('library.txt'))
            db.create_file()
            return db
        elif db == '2' or db.lower() == 'sqlite':
            db = SqliteDatabase('library.db')
            db.create_table()
            return db
        elif db == '3' or db.lower() == 'exit':
            return None

def get_operation() -> str:
    """Функция выводит пользователю список доступных операций. Возвращает выбранную пользователем операцию или None,
    если клиент ввел '6' или 'exit' """

    operations = ('\nСписок доступных операций: \n'
                  '1: 1 или add - добавить книгу в базу данных\n'
                  '2: 2 или delete - удалить книгу из базы данных\n'
                  '3: 3 или search - поиск книги в базе данных\n'
                  '4: 4 или all - вывод всех книг из базы данных\n'
                  '5: 5 или status - сменить статус книги\n'
                  '6: 6 или exit - выход из базы данных\n'
                  'Для выхода из операции после начала работы в поле ввода введите "/exit"\n')

    available_operations = ('1', '2', '3', '4', '5', '6', 'add', 'delete', 'search', 'all', 'status', 'exit')
    print(operations)

    # Запрос желаемой операции от пользователя
    while True:
        operation = input('Введите операцию: ')
        if operation.lower() in available_operations:
            return operation.lower()

def add() -> dict | None:
    """Функция запрашивает у пользователя название книги, фамилию и инициалы автора, год издания книги. Возвращает
    словарь с полученными данными или None, если на любом из этапов ввода пользователь ввел '/exit' """
    data_dict = {}

    # запрос названия книги
    while True:
        title = input('Введите название книги: ')
        # проверка на выход из операции
        if title == '/exit':
            return None
        # не вижу смысла проверять ввод на title, я считаю, что название у книги может содержать любые символы
        if title:
            data_dict['title'] = title
            break

    # запрос фамилии и инициалов
    while True:
        second_name = input('Введите фамилию автора книги: ')
        # проверка на выход из операции
        if second_name == '/exit':
            return None
        # проверка, все ли символы в second_name текстовые
        if second_name.isalpha():
            initials = input('Введите инициалы автора (в формате А.А.): ')
            if initials == '/exit':
                return None
            # проверка формата ввода инициалов (тут не учтено, что могут быть переданы инициалы в формате "Ал.С.")
            if len(initials) == 4 and (initials[1] == '.' and initials[-1] == '.'):
                author = second_name.lower().capitalize() + ' ' + initials.upper()
                data_dict['author'] = author
                break

    # запрос года издания книги
    while True:
        year = input('Введите год издания книги: ')
        # проверка на выход из операции
        if year == '/exit':
            return None
        # проверка, являются ли символы в year числовые
        if year.isdigit():
            year = int(year)
            data_dict['year'] = year
            break
    return data_dict

def delete() -> int | None:
    # запрос book_id
    while True:
        # проверка корректности введенного book_id
        book_id = input('Введите id книги, которую хотите удалить: ')
        # проверка на выход из операции
        if book_id == '/exit':
            return None
        if book_id.isdigit():
            return int(book_id)

def search() -> dict | None:
    print('Поиск доступен по title, author, year. Искать можно как по каждому отдельно взятому критерию, '
          'так и по их комбинации. Для пропуска критерия вводите пустое значение.')
    data_dict = {}
    # не вижу смысла проверять ввод на title, я считаю, что название у книги может содержать любые символы
    title = input('Введите название книги: ')
    # проверка на выход из операции
    if title == '/exit':
        return None
    if title:
        data_dict['title'] = title
    # Запрос фамилии автора. Здесь не запрашиваются точные данные, т.к. в бд ищутся вхождения данных, введенных ниже
    while True:
        second_name = input('Введите фамилию автора книги: ')
        # проверка на выход из операции
        if second_name == '/exit':
            return None
        # Проверка на пустое значение
        if not second_name:
            break
        # проверка, все ли символы в second_name текстовые
        if second_name.isalpha():
            data_dict['author'] = second_name.lower().capitalize()
            break

    while True:
        year = input('Введите год издания книги: ')
        # проверка на выход из операции
        if year == '/exit':
            return None
        # проверка на пустое значение
        if not year:
            break
        # проверка, являются ли символы в year числовые
        if year.isdigit():
            year = int(year)
            data_dict['year'] = year
            break
    return data_dict

def status() -> dict | None:
    data_dict = {}
    # Получение book_id
    while True:
        book_id = input('Введите id книги, статус которой хотите поменять: ')
        # проверка на выход из операции
        if book_id == '/exit':
            return None
        # проверка корректности введенного book_id
        if book_id.isdigit():
            data_dict['book_id'] = int(book_id)
            break
    # получение new_status
    while True:
        new_status = input('Введите новый статус: ')
        # проверка на выход из операции
        if new_status == '/exit':
            return None
        # проверка корректности введенного статуса
        available_statuses = ('в наличии', 'выдана')
        if new_status.lower() not in available_statuses:
            print('Введен некорректный статус.')
        else:
            data_dict['new_status'] = new_status.lower()
            break

    return data_dict

