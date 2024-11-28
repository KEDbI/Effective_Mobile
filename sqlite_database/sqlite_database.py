import sqlite3

class SqliteDatabase:
    def __init__(self, db_name: str, table_name: str = 'library') -> None:
        self.db_name = db_name
        self.table_name = table_name

    def create_table(self) -> None:
        """Функция для создания таблицы в бд"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}('
                                    'book_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                                    'title TEXT NOT NULL,'
                                    'author TEXT NOT NULL,'
                                    'year INTEGER NOT NULL,'
                                    'status TEXT NOT NULL DEFAULT "в наличии")')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')

    def add_book(self, title: str, author: str, year: int) -> None:
        """Функция для добавления книги бд"""
        try:
            # Подключение к бд
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Вставка данных в бд
                cursor.execute(f'INSERT INTO {self.table_name} (title, author, year)'
                               f'VALUES (?, ?, ?)', (title, author, year))
                # Поиск вставленной строки для вывода пользователю
                cursor.execute(f'SELECT * FROM {self.table_name} '
                               f'WHERE book_id=(SELECT MAX(book_id) FROM {self.table_name})')
                book = cursor.fetchone()
                print(f'id: {book[0]}, title: {book[1]}, author: {book[2]}, year: {book[3]}, status: {book[4]}')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')

    def delete_book(self, book_id: int) -> None:
        """Функция для удаления книги из бд"""
        try:
            # Подключение к бд
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Проверка наличия полученного book_id в бд
                cursor.execute(f'SELECT * from {self.table_name} WHERE book_id={book_id}')
                if cursor.fetchone():
                    # Если полученный book_id есть в бд, удаляем нужную строку
                    cursor.execute(f'DELETE FROM {self.table_name} WHERE book_id=?', (book_id,))
                    print(f'Книга с id {book_id} удалена.')
                else:
                    print('Книги с таким id нет.')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')

    def search_books(self, title: str | None = None, author: str | None = None, year: int | None = None) -> None:
        """Функция для поиска книги по title, author, year. Искать можно как по каждому отдельно взятому критерию,
        так и по их комбинации"""
        params = {}
        # проверка введенных данных, добавление их в словарь params
        if title:
            params['title'] = title + '%'
        if author:
            # символ % здесь нужен для поиска с конструкцией LIKE
            params['author'] = author + '%'
        if year:
            params['year'] = year
        columns = [i for i in params.keys()]
        values = tuple([i for i in params.values()])
        try:
            # Подключение к бд
            with sqlite3.connect(self.db_name) as conn:
                # Т.к. мы не знаем, какое количество параметров будет передано в функцию, запрос к бд формируем
                # динамически, в зависимости от параметров
                query = (f'SELECT * FROM {self.table_name} '
                         f'WHERE ')
                for i in columns:
                    if i != 'year':
                        query += i + f' LIKE ?' + ' AND '
                    else:
                        query += i + '=? AND '
                query = query.rstrip(' AND ')
                cursor = conn.cursor()
                # Получение результатов поиска и вывод их пользователю
                cursor.execute(query, values)
                res = tuple([book for book in cursor.fetchall()])
                if res:
                    for book in res:
                        print(f'id: {book[0]}, title: {book[1]}, author: {book[2]}, year: {book[3]}, status: {book[4]}')
                else:
                    print('По заданным критериям книг не найдено.')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')


    def get_all_books(self) -> None:
        """Функция для вывода всех книг из бд"""
        try:
            # Подключение к бд
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Получение результатов и вывод их пользователю
                cursor.execute(f'SELECT * FROM {self.table_name}')
                books = cursor.fetchall()
                for book in books:
                    print(f'id: {book[0]}, title: {book[1]}, author: {book[2]}, year: {book[3]}, status: {book[4]}')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')

    def change_status(self, book_id: int, new_status: str) -> None:
        """Функция для смены статуса книги"""
        try:
            # Подключение к бд
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Проверка наличия полученного book_id в бд
                cursor.execute(f'SELECT * from {self.table_name} WHERE book_id={book_id}')
                if cursor.fetchone():
                    # Если полученный book_id есть в бд, обновляем нужную строку
                    cursor.execute(f'UPDATE {self.table_name} set status=? '
                                   f'WHERE book_id=?', (new_status, book_id))
                    # Поиск обновленной строки для вывода пользователю
                    cursor.execute(f'SELECT * FROM {self.table_name} '
                                   f'WHERE book_id=?', (book_id,))
                    book = cursor.fetchone()
                    print(f'id: {book[0]}, title: {book[1]}, author: {book[2]}, year: {book[3]}, status: {book[4]}')
                else:
                    print('Книги с таким id нет.')
        except sqlite3.Error:
            print('При работе с базой данных произошла ошибка, попробуйте позже.')



