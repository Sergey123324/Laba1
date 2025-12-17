from librarycard import LibraryCard
import Errors


class Library:
    def __init__(self):
        self.books = []
        self.readers = []
        self.cards = []

    def add_reader(self, reader):
        try:
            for r in self.readers:
                if r.reader_id == reader.reader_id:
                    raise Errors.ReaderAlreadyExistsError(f"Читатель с ID {reader.reader_id} уже существует!")

            self.readers.append(reader)
            card = LibraryCard(reader)
            self.cards.append(card)
            return card

        except Errors.ReaderAlreadyExistsError as e:
            print(f"Ошибка: {e}")
            return None

    def add_book(self, book):
        try:
            for b in self.books:
                if b.isbn == book.isbn:
                    raise Errors.BookYetAlreadyError(f"Книга с ISBN {book.isbn} уже существует!")

            self.books.append(book)
            return book

        except Errors.BookYetAlreadyError as e:
            print(f"Ошибка: {e}")
            return None

    def search_book(self, search_term):
        try:
            found_books = []
            for book in self.books:
                if (search_term.lower() in book.title.lower() or
                        search_term.lower() in book.author.name.lower()):
                    found_books.append(book)

            if not found_books:
                raise Errors.BookNotFoundError(f"Книги по запросу '{search_term}' не найдены!")

            return found_books

        except Errors.BookNotFoundError as e:
            print(f"Ошибка: {e}")
            return []

    def borrow_book(self, reader_id, book_title):
        try:
            reader_card = None
            for card in self.cards:
                if card.reader.reader_id == reader_id:
                    reader_card = card
                    break

            if not reader_card:
                raise Errors.ReaderNotFoundError(f"Читатель с ID {reader_id} не найден!")

            book_to_borrow = None
            for book in self.books:
                if book.title == book_title and book.available:
                    book_to_borrow = book
                    break

            if not book_to_borrow:
                raise Errors.BookNotAvailableError(f"Книга '{book_title}' недоступна для выдачи!")

            if reader_card.borrow_book(book_to_borrow):
                print(f"Книга '{book_title}' выдана читателю {reader_card.reader.card()}")
                return True

        except (Errors.ReaderNotFoundError, Errors.BookNotAvailableError) as e:
            print(f"Ошибка: {e}")
            return False

    def return_book(self, reader_id, book_title):
        try:
            reader_card = None
            for card in self.cards:
                if card.reader.reader_id == reader_id:
                    reader_card = card
                    break

            if not reader_card:
                raise Errors.ReaderNotFoundError(f"Читатель с ID {reader_id} не найден!")

            for book in reader_card.borrowed_books:
                if book.title == book_title:
                    if reader_card.return_book(book):
                        print(f"Книга '{book_title}' возвращена")
                        return True

            raise Errors.BookNotFoundError(f"Книга '{book_title}' не найдена у читателя!")

        except (Errors.ReaderNotFoundError, Errors.BookNotFoundError) as e:
            print(f"Ошибка: {e}")
            return False

    def list_available_books(self):
        available_books = [book for book in self.books if book.available]
        return available_books

    def to_dict(self):
        return {
            "books": [book.to_dict() for book in self.books],
            "readers": [reader.to_dict() for reader in self.readers],
            "library_cards": [card.to_dict() for card in self.cards]
        }