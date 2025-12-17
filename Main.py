from library import Library
from reader import Reader
from book import Book
from author import Author
from json_handler import JSONHandler
from xml_handler import XMLHandler
import Errors


def main():
    library = Library()

    print("=" * 50)
    print("БИБЛИОТЕЧНАЯ СИСТЕМА")
    print("=" * 50)

    load_choice = input("Хотите загрузить данные из файла? (y/n): ").strip().lower()
    if load_choice == 'y':
        format_choice = input("Из какого формата загрузить? (1-JSON, 2-XML): ").strip()
        if format_choice == '1':
            JSONHandler.load_library_data(library)
        elif format_choice == '2':
            XMLHandler.load_library_data(library)

    if not library.books:
        init_test_data(library)

    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ")
        print("=" * 50)
        print("1. Добавить книгу")
        print("2. Найти книгу")
        print("3. Зарегистрировать читателя")
        print("4. Выдать книгу")
        print("5. Вернуть книгу")
        print("6. Показать доступные книги")
        print("7. Показать всех читателей")
        print("8. Показать книги на руках у читателя")
        print("9. Сохранить данные в JSON")
        print("10. Сохранить данные в XML")
        print("11. Загрузить данные из JSON")
        print("12. Загрузить данные из XML")
        print("0. Выход")
        print("-" * 50)

        try:
            choice = input("Выберите действие (0-12): ").strip()

            if choice == "1":
                add_book_flow(library)
            elif choice == "2":
                search_book_flow(library)
            elif choice == "3":
                register_reader_flow(library)
            elif choice == "4":
                borrow_book_flow(library)
            elif choice == "5":
                return_book_flow(library)
            elif choice == "6":
                list_available_books_flow(library)
            elif choice == "7":
                list_readers_flow(library)
            elif choice == "8":
                show_reader_books_flow(library)
            elif choice == "9":
                JSONHandler.save_library_data(library)
            elif choice == "10":
                XMLHandler.save_library_data(library)
            elif choice == "11":
                JSONHandler.load_library_data(library)
            elif choice == "12":
                XMLHandler.load_library_data(library)
            elif choice == "0":
                save_before_exit = input("Сохранить данные перед выходом? (y/n): ").strip().lower()
                if save_before_exit == 'y':
                    format_choice = input("В каком формате сохранить? (1-JSON, 2-XML, 3-оба): ").strip()
                    if format_choice in ['1', '3']:
                        JSONHandler.save_library_data(library)
                    if format_choice in ['2', '3']:
                        XMLHandler.save_library_data(library)
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Введите число от 0 до 12.")

        except KeyboardInterrupt:
            print("\n\nПрограмма завершена пользователем.")
            break
        except Exception as e:
            print(f"\nНепредвиденная ошибка: {type(e).__name__}: {e}")
            print("Программа продолжает работу...")


def add_book_flow(library):
    print("\n--- Добавление новой книги ---")
    try:
        title = input("Название книги: ").strip()
        if not title:
            print("Название не может быть пустым!")
            return

        author_name = input("Имя автора: ").strip()
        author_country = input("Страна автора: ").strip()

        isbn = input("ISBN (например, 978-5-389-07435-2): ").strip()
        if not isbn:
            print("ISBN обязателен!")
            return

        year_str = input("Год издания: ").strip()
        try:
            year = int(year_str)
            if year < 0 or year > 2025:
                raise ValueError("Некорректный год")
        except ValueError:
            print("Год должен быть числом!")
            return

        author = Author(author_name, author_country)
        book = Book(title, author, isbn, year)

        result = library.add_book(book)
        if result:
            print(f"Книга '{title}' успешно добавлена!")

    except Exception as e:
        print(f"Ошибка при добавлении книги: {e}")


def search_book_flow(library):
    print("\n--- Поиск книги ---")
    try:
        search_term = input("Введите название книги или автора: ").strip()
        if not search_term:
            print("Введите поисковый запрос!")
            return

        found_books = library.search_book(search_term)
        if found_books:
            print(f"\nНайдено {len(found_books)} книг:")
            for i, book in enumerate(found_books, 1):
                print(f"{i}. {book.info()}")
        else:
            print("По вашему запросу ничего не найдено")

    except Exception as e:
        print(f"Ошибка при поиске: {e}")


def register_reader_flow(library):
    print("\n--- Регистрация нового читателя ---")
    try:
        name = input("Имя читателя: ").strip()
        surname = input("Фамилия читателя: ").strip()

        if not name or not surname:
            print("Имя и фамилия обязательны!")
            return

        reader_id = input("ID читателя (например, R001): ").strip()
        if not reader_id:
            print("ID обязателен!")
            return

        reader = Reader(name, surname, reader_id)

        card = library.add_reader(reader)
        if card:
            print(f"Читатель {name} {surname} успешно зарегистрирован!")
            print(f"Выдан читательский билет")

    except Exception as e:
        print(f"Ошибка при регистрации: {e}")


def borrow_book_flow(library):
    print("\n--- Выдача книги читателю ---")
    try:
        available = library.list_available_books()
        if not available:
            print("Нет доступных книг для выдачи!")
            return

        print("\nДоступные книги:")
        for i, book in enumerate(available, 1):
            print(f"{i}. {book.title} - {book.author.name}")

        book_index = input("\nВведите номер книги для выдачи (или 0 для отмены): ").strip()
        if book_index == "0":
            print("Отмена операции.")
            return

        try:
            book_index = int(book_index) - 1
            if book_index < 0 or book_index >= len(available):
                print("Неверный номер книги!")
                return
            selected_book = available[book_index]
        except ValueError:
            print("Введите номер!")
            return

        reader_id = input("Введите ID читателя: ").strip()

        success = library.borrow_book(reader_id, selected_book.title)

    except Exception as e:
        print(f"Ошибка при выдаче книги: {e}")


def return_book_flow(library):
    print("\n--- Возврат книги ---")
    try:
        reader_id = input("Введите ID читателя: ").strip()
        if not reader_id:
            print("Введите ID читателя!")
            return

        reader_card = None
        for card in library.cards:
            if card.reader.reader_id == reader_id:
                reader_card = card
                break

        if not reader_card:
            print(f"Читатель с ID {reader_id} не найден!")
            return

        if not reader_card.borrowed_books:
            print("У читателя нет книг для возврата!")
            return

        print("\nКниги на руках у читателя:")
        for i, book in enumerate(reader_card.borrowed_books, 1):
            print(f"{i}. {book.title}")

        book_index = input("\nВведите номер книги для возврата (или 0 для отмены): ").strip()
        if book_index == "0":
            print("Отмена операции.")
            return

        try:
            book_index = int(book_index) - 1
            if book_index < 0 or book_index >= len(reader_card.borrowed_books):
                print("Неверный номер книги!")
                return
            selected_book = reader_card.borrowed_books[book_index]
        except ValueError:
            print("Введите номер!")
            return

        success = library.return_book(reader_id, selected_book.title)

    except Exception as e:
        print(f"Ошибка при возврате книги: {e}")


def list_available_books_flow(library):
    print("\n--- Доступные книги ---")
    try:
        available = library.list_available_books()
        if not available:
            print("Нет доступных книг")
        else:
            print(f"Всего доступно: {len(available)} книг")
            for i, book in enumerate(available, 1):
                print(f"{i}. {book.info()}")
    except Exception as e:
        print(f"Ошибка: {e}")


def list_readers_flow(library):
    print("\n--- Зарегистрированные читатели ---")
    try:
        if not library.readers:
            print("Нет зарегистрированных читателей")
        else:
            print(f"Всего читателей: {len(library.readers)}")
            for i, reader in enumerate(library.readers, 1):
                print(f"{i}. {reader.surname} {reader.name} (ID: {reader.reader_id})")
    except Exception as e:
        print(f"Ошибка: {e}")


def show_reader_books_flow(library):
    print("\n--- Книги на руках у читателя ---")
    try:
        reader_id = input("Введите ID читателя: ").strip()

        for card in library.cards:
            if card.reader.reader_id == reader_id:
                card.show_borrowed_books()
                return

        print(f"Читатель с ID {reader_id} не найден")

    except Exception as e:
        print(f"Ошибка: {e}")


def init_test_data(library):
    try:
        print("\n--- Создание тестовых данных ---")

        authors = [
            Author("Лев Толстой", "Россия"),
            Author("Фёдор Достоевский", "Россия"),
            Author("Антон Чехов", "Россия"),
            Author("Айзек Азимов", "США")
        ]

        books = [
            Book("Война и мир", authors[0], "978-5-389-07435-2", 1869),
            Book("Анна Каренина", authors[0], "978-5-699-40115-1", 1877),
            Book("Преступление и наказание", authors[1], "978-5-17-060692-6", 1866),
            Book("Идиот", authors[1], "978-5-17-090690-3", 1869),
            Book("Вишневый сад", authors[2], "978-5-08-005407-7", 1904),
            Book("Я, робот", authors[3], "978-5-699-30670-2", 1950)
        ]

        for book in books:
            library.add_book(book)

        readers = [
            Reader("Иван", "Петров", "R001"),
            Reader("Мария", "Сидорова", "R002"),
            Reader("Алексей", "Иванов", "R003")
        ]

        for reader in readers:
            library.add_reader(reader)

        library.borrow_book("R001", "Война и мир")
        library.borrow_book("R002", "Я, робот")

        print("Тестовые данные созданы:")
        print(f"  Книг в библиотеке: {len(library.books)}")
        print(f"  Читателей: {len(library.readers)}")

    except Exception as e:
        print(f"Ошибка создания тестовых данных: {e}")


if __name__ == "__main__":
    main()