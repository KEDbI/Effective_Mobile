from user_interaction.user_interaction import start, get_operation, add, delete, search, status


def main() -> None:
    # вызов функции start() и присваивание выбранной пользователем бд переменной db. Если пользователь введет '3' или
    # 'exit', функция вернет None
    while True:
        db = start()
        if db:
            while True:

                # получение операции от пользователя
                operation = get_operation()

                # В зависимости от выбранной операции дергаются необходимые функции из модуля user_interaction.
                # Эти функции возвращают словарь с данными, введенными пользователем. Затем дергаются функции из
                # модуля с бд, в качестве аргументов в эти функции распаковывается словарь, полученный выше.
                # Функции из модуля user_interaction могут вернуть None в том случае,
                # когда юзер в поле ввода введет команду '/exit', тогда пользователю снова выведутся доступные команды,
                # а все данные, которые он ввел, не сохранятся.

                if operation == '1' or operation.lower() == 'add':
                    string_to_db = add()
                    if string_to_db:
                        db.add_book(**string_to_db)

                if operation == '2' or operation.lower() == 'delete':
                    book_id = delete()
                    if book_id:
                        db.delete_book(book_id)

                if operation == '3' or operation.lower() == 'search':
                    search_db = search()
                    # здесь одновременно идет проверка и на '/exit', и на пустой словарь (если пользователь не ввел никаких данных)
                    if search_db:
                        db.search_books(**search_db)

                if operation == '4' or operation.lower() == 'all':
                    # здесь ничего объяснять пользователю не надо и не требуются данные от пользователя, поэтому
                    # функции all() в user_interaction нет, сразу идет запрос в бд и вывод в консоль
                    db.get_all_books()

                if operation == '5' or operation.lower() == 'status':
                    change_status = status()
                    if change_status:
                        db.change_status(**change_status)

                if operation == '6' or operation.lower() == 'exit':
                    break
        else:
            return None


if __name__ == '__main__':
    main()