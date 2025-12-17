from book import Book


class LibraryCard:
    def __init__(self, reader):
        self.reader = reader
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.available = True
            self.borrowed_books.remove(book)
            return True
        return False

    def show_borrowed_books(self):
        if not self.borrowed_books:
            print(f"У читателя {self.reader.card()} нет книг")
        else:
            print(f"Книги у читателя {self.reader.card()}:")
            for i, book in enumerate(self.borrowed_books, 1):
                print(f"{i}. {book.info()}")

    def to_dict(self):
        return {
            "reader": self.reader.to_dict(),
            "borrowed_books": [book.to_dict() for book in self.borrowed_books]
        }