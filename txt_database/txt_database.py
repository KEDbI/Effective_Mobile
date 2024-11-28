from pathlib import Path

class Library:
    def __init__(self, db_file: Path):
        self.db_file = db_file

    def create_file(self) -> None:
        try:
            self.db_file.touch()
            return None
        except FileExistsError:
            return None


    def _get_db_list(self) -> list:
        """Функция для преобразования строк из текстового файла в список"""
        if self.db_file.read_text():
            db: list = self.db_file.read_text().split('\n')
        else:
            db: list = []
        return db

    def _write_to_file(self, db_list: list) -> None:
        """Функция для записи строк в файл"""
        with self.db_file.open(mode='w') as file:
            lines = '\n'.join(db_list).lstrip('\n')
            file.write(lines)

    def _get_available_ids(self, db_list: list [str | int]):
        """Вспомогательная функция для функции add_book, возвращает список недостающих book_id
        или пустой список, если недостающих book_id нет (например, у нас файле есть book_id от 1 до 9, пользователь
        удаляет строку с book_id 2 и 4, эта функция вернет список [2,4]"""
        ids_in_db = self._get_db_ids(db_list)
        available_ids = list(set(num for num in range(1, len(db_list)+2)) - set(ids_in_db))
        return available_ids

    @staticmethod
    def _get_db_ids(db_list: list[str | int]) -> list:
        """Вспомогательная функция для функции get_available_ids и delete_book,
        возвращает список book_id из текстового файла"""
        ids_in_db = []
        for i in db_list:
            # деление строки из файла на подстроки
            for j in str(i).split(', '):
                # поиск подстроки с id
                if 'id' in j:
                    book_id = ''
                    # поиск числовых значений
                    for symbol in j:
                        try:
                            book_id  += str(int(symbol))
                        except ValueError:
                            continue
                    ids_in_db.append(int(book_id))
        return ids_in_db



    def add_book(self, title: str, author: str, year: int) -> None:
        """Функция для добавления книги в текстовый файл"""
        db = self._get_db_list()
        available_ids = self._get_available_ids(db)
        # проверка доступных book_id, если есть, то присваиваем строке первый доступный id, если нет,
        # то присваиваем строке id, равный количеству строк в файле +1
        if available_ids:
            book = f'id: {available_ids[0]}, title: {title}, author: {author}, year: {year}, status: в наличии'
            db.append(book)
        else:
            book = f'id: {len(db)+1}, title: {title}, author: {author}, year: {year}, status: в наличии'
            db.append(book)
        self._write_to_file(db)
        print(f'Книга добавлена: \n{book}')


    def delete_book(self, book_id: int) -> None:
        """Функция для удаления строки из файла"""
        db = self._get_db_list()
        ids_in_db = self._get_db_ids(db)
        if book_id in ids_in_db:
            for i in db:
                # поиск строки с нужным book_id
                for j in str(i).split(', '):
                    if f'id: {book_id}' in j:
                        db.remove(i)
            self._write_to_file(db)
            print(f'Книга с id {book_id} удалена.')
        else:
            print('Книги с таким id нет.')

    def search_books(self, title: str | None = None, author: str | None = None, year: int | None = None) -> None:
        """Функция для поиска книги по title, author, year. Искать можно как по каждому отдельно взятому критерию,
        так и по их комбинации"""
        db = self._get_db_list()
        search_string = ''
        # проверка введенных данных, добавление их в строку search_string
        if title:
            search_string += f'title: {title}, '
        if author:
            search_string += f'author: {author}, '
        if year:
            search_string += f'year: {year}, '
        search_string = search_string.rstrip(', ')
        result = []
        # поиск вхождения строки search_string в стрОки из текстового файла
        for i in db:
            if search_string in i:
                result.append(i)
        if result:
            for i in result:
                print(i)
        else:
            print('По заданным критериям книг не найдено.')

    def get_all_books(self) -> None:
        """Функция для вывода всех строк из текстового файла"""
        print(self.db_file.read_text())

    def change_status(self, book_id: int, new_status: str) -> None:
        """Функция для смены статуса книги"""
        # Функция выглядит перегруженной, возможно, стоило поделить ее на более мелкие функции

        db = self._get_db_list()
        ids_in_db = self._get_db_ids(db)
        # проверка book_id
        if book_id in ids_in_db:
            # поиск строки с нужным book_id
            for i, value1 in enumerate(db):
                if f'id: {book_id}' in value1:
                    # Преобразование нужной строки в список подстрок
                    line_list = str(value1).split(', ')
                    # Поиск подстроки со статусом
                    for j, value2 in enumerate(line_list):
                        if 'status' in value2:
                            # Редактирование подстроки со статусом
                            value2 = f'status: {new_status}'
                            line_list[j] = value2
                            # Преобразование подстрок в строку и внесение изменений в db_list
                            line = ', '.join(line_list)
                            db[i] = line
                            print('Статус изменен:\n' + db[i])
            self._write_to_file(db)
        else:
            print('Книги с таким id нет.')

