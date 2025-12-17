from library import Library
from librarycard import LibraryCard
from reader import Reader
from book import Book
from author import Author
from Errors import *


def main():
    library = Library()

    init_test_data(library)

    while True:
        print("\n" + "=" * 50)
        print(" БИБЛИОТЕЧНАЯ СИСТЕМА")
        print("=" * 50)
        print("1.  Добавить книгу")
        print("2.  Найти книгу")
        print("3.  Зарегистрировать читателя")
        print("4.  Выдать книгу")
        print("5.  Вернуть книгу")
        print("6.  Показать доступные книги")
        print("7.  Показать книги на руках у читателя")
        print("8.  Сохранить данные в JSON (для лабораторной)")
        print("9.  Сохранить данные в XML (для лабораторной)")
        print("0.  Выход")
        print("-" * 50)

        try:
            choice = input("Выберите действие (0-9): ").strip()

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
                save_to_json_flow(library)
            elif choice == "0":
                print("До свидания! ")
                break
            else:
                print(" Неверный выбор. Введите число от 0 до 9.")

        except KeyboardInterrupt:
            print("\n\nПрограмма завершена пользователем.")
            break
        except Exception as e:
            print(f"\n  Непредвиденная ошибка: {type(e).__name__}: {e}")
            print("Программа продолжает работу...")

def add_book_flow(library):
    print("\n--- Добавление новой книги ---")
    try:
        title = input("Название книги: ").strip()
        if not title:
            print(" Название не может быть пустым!")
            return

        author_name = input("Имя автора: ").strip()
        author_country = input("Страна автора: ").strip()

        isbn = input("ISBN (например, 978-5-389-07435-2): ").strip()
        if not isbn:
            print(" ISBN обязателен!")
            return

        year_str = input("Год издания: ").strip()
        try:
            year = int(year_str)
            if year < 0 or year > 2025:
                raise ValueError("Некорректный год")
        except ValueError:
            print(" Год должен быть числом!")
            return

        author = Author(author_name, author_country)
        book = Book(title, author, isbn, year)

        result = library.add_book(book)
        if result:
            print(f" Книга '{title}' успешно добавлена!")

    except Exception as e:
        print(f" Ошибка при добавлении книги: {e}")


def search_book_flow(library):
    print("\n--- Поиск книги ---")
    try:
        search_term = input("Введите название книги или автора: ").strip()
        if not search_term:
            print(" Введите поисковый запрос!")
            return

        found_books = library.search_book(search_term)
        if found_books:
            print(f"\n Найдено {len(found_books)} книг")
        else:
            print(" По вашему запросу ничего не найдено")

    except Exception as e:
        print(f" Ошибка при поиске: {e}")


def register_reader_flow(library):
    print("\n--- Регистрация нового читателя ---")
    try:
        name = input("Имя читателя: ").strip()
        surname = input("Фамилия читателя: ").strip()

        if not name or not surname:
            print(" Имя и фамилия обязательны!")
            return

        reader_id = input("ID читателя (например, R001): ").strip()
        if not reader_id:
            print(" ID обязателен!")
            return

        reader = Reader(name, surname, reader_id)

        card = library.add_reader(reader)
        if card:
            print(f" Читатель {name} {surname} успешно зарегистрирован!")
            print(f" Выдан читательский билет")

    except ReaderAlreadyExistsError as e:
        print(f" {e}")
    except Exception as e:
        print(f" Ошибка при регистрации: {e}")


def borrow_book_flow(library):
    print("\n--- Выдача книги читателю ---")
    try:
        available = library.list_available_books()
        if not available:
            print(" Нет доступных книг для выдачи!")
            return

        book_index = input("\nВведите номер книги для выдачи (или 0 для отмены): ").strip()
        if book_index == "0":
            print("Отмена операции.")
            return

        try:
            book_index = int(book_index) - 1
            if book_index < 0 or book_index >= len(available):
                print(" Неверный номер книги!")
                return
            selected_book = available[book_index]
        except ValueError:
            print(" Введите номер!")
            return

        reader_id = input("Введите ID читателя: ").strip()

        if hasattr(library, 'borrow_book'):
            success = library.borrow_book(reader_id, selected_book.title)
        else:
            print("  Метод выдачи книги пока не реализован в библиотеке")
            print(f"Книга '{selected_book.title}' будет выдана позже")
            success = True

        if success:
            print(f" Книга '{selected_book.title}' выдана читателю ID: {reader_id}")

    except Exception as e:
        print(f" Ошибка при выдаче книги: {e}")


def return_book_flow(library):
    print("\n--- Возврат книги ---")
    try:

        book_title = input("Введите название возвращаемой книги: ").strip()
        if not book_title:
            print(" Введите название книги!")
            return

        print("  Функция возврата книги требует реализации в классе Library")
        print("Сейчас книга будет просто отмечена как доступная")

        for book in library.books:
            if book.title.lower() == book_title.lower():
                if not book.available:
                    book.available = True
                    print(f" Книга '{book.title}' возвращена в библиотеку")
                else:
                    print(f"  Книга '{book.title}' уже была в библиотеке")
                return

        print(f" Книга '{book_title}' не найдена в библиотеке")

    except Exception as e:
        print(f" Ошибка при возврате книги: {e}")


def list_available_books_flow(library):
    print("\n--- Доступные книги ---")
    try:
        available = library.list_available_books()
        if not available:
            print(" Нет доступных книг")
        else:
            print(f" Всего доступно: {len(available)} книг")
    except Exception as e:
        print(f" Ошибка: {e}")


def list_readers_flow(library):
    print("\n--- Зарегистрированные читатели ---")
    try:
        if not library.readers:
            print(" Нет зарегистрированных читателей")
        else:
            print(f"👥 Всего читателей: {len(library.readers)}")
            for i, reader in enumerate(library.readers, 1):
                print(f"{i}. {reader.surname} {reader.name} (ID: {reader.reader_id})")
    except Exception as e:
        print(f" Ошибка: {e}")


def show_reader_books_flow(library):
    print("\n--- Книги на руках у читателя ---")
    try:
        reader_id = input("Введите ID читателя: ").strip()

        for card in library.cards if hasattr(library, 'cards') else []:
            if card.reader.reader_id == reader_id:
                card.show_borrowed_books()
                return

        print(f" Читатель с ID {reader_id} не найден или у него нет читательского билета")

    except Exception as e:
        print(f" Ошибка: {e}")


def save_to_json_flow(library):
    print("\n--- Сохранение данных в JSON ---")
    try:
        import json
        import os

        data = {
            "books": [],
            "readers": []
        }

        for book in library.books:
            book_data = {
                "title": book.title,
                "author": {
                    "name": book.author.name,
                    "country": book.author.country
                },
                "isbn": book.isbn,
                "year": book.year,
                "available": book.available
            }
            data["books"].append(book_data)

        for reader in library.readers:
            reader_data = {
                "name": reader.name,
                "surname": reader.surname,
                "reader_id": reader.reader_id
            }
            data["readers"].append(reader_data)

        filename = "library_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f" Данные сохранены в файл: {filename}")
        print(f" Статистика: {len(data['books'])} книг, {len(data['readers'])} читателей")

    except PermissionError:
        print(" Ошибка: нет прав для записи файла")
    except Exception as e:
        print(f" Ошибка при сохранении: {e}")


def init_test_data(library):
    try:
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

        if hasattr(library, 'borrow_book'):
            library.borrow_book("R001", "Война и мир")
            library.borrow_book("R002", "Я, робот")

        print(" Тестовые данные загружены")
        print(f" Книг в библиотеке: {len(library.books)}")
        print(f" Читателей: {len(library.readers)}")

    except Exception as e:
        print(f"⚠️  Ошибка загрузки тестовых данных: {e}")


if __name__ == "__main__":
    main()