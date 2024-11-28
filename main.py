from user_interaction.user_interaction import start, get_operation, add, delete, search, status


def main() -> None:
    # вызов функции start() и присваивание выбранной юзером бд переменной db
    while True:
        db = start()
        if db:
            while True:
                # получение операции от юзера
                operation = get_operation()
                # В зависимости от выбранной операции дергаются необходимые функции. Эти функции могут вернуть None
                # в том случае, когда юзер в поле ввода введет команду '/exit', тогда юзеру снова выведутся доступные
                # команды, а все данные, которые он ввел, не сохранятся
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
                    if search_db:
                        db.search_books(**search_db)

                if operation == '4' or operation.lower() == 'all':
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