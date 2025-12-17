from librarycard import LibraryCard
from reader import Reader
from book import Book
import Errors

class Library:
    def init(self):
        self.books = []
        self.readers = []

    def add_reader(self,reader):
        try:
            if reader in self.readers:
                raise Errors.ReaderAlreadyExistsError(f"Читатель {reader.name} уже зарегистрирован!")
            self.readers.append(reader)
            print(f"Читатель {reader.name} успешно добавлен.")
            return LibraryCard(reader)
        except Errors.ReaderAlreadyExistsError as e:
            print(f"Ошибка: {e}")
            return None

    def add_book(self, book):
        try:
            if book in self.books:
                raise Errors.BookYetAlreadyError(f"Книга {book.title} уже есть в каталоге!")
            self.books.append(book)
            print(f"Книга {book.title} успешно добавлена.")
            return self.books
        except Errors.BookYetAlreadyError as e:
            print(f"Ошибка: {e}")
            return None

    def search_book(self, title):
        try:
            found_books = []
            for book in self.books:
                if title.lower() in book.title.lower():
                    found_books.append(book)

            if not found_books:
                raise Errors.BookNotFoundError(f"Книга с названием '{title}' не найдена!")

            print(f"Найдено книг: {len(found_books)}")
            for book in found_books:
                print(f"  - {book.title} ({'Доступна' if book.available else 'Выдана'})")
            return found_books

        except Errors.BookNotFoundError as e:
            print(f"Ошибка: {e}")
            return []

    def list_available_books(self):
        available_books = []
        try:
            for book in self.books:
                if book.available:
                    available_books.append(book)

            if not available_books:
                print("Нет доступных книг в библиотеке.")
            else:
                print(f"Доступных книг: {len(available_books)}")
                for i, book in enumerate(available_books, 1):
                    print(f"{i}. '{book.title}' - {book.author.name}")

            return available_books

        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return []
