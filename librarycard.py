from reader import Reader
from book import Book

class LibraryCard:
    def init(self, reader):
        self.reader = reader
        self.list_of_borrowed_books = []

    def borrowed_book(self, book):
        if book.available:
            book.available = False
            self.list_of_borrowed_books.append(book)
            print(f"{book.title} выдана {self.reader}!")
        else:
            print(f"Книги нет в наличии!")

    def return_book(self, book):
        if book in self.list_of_borrowed_books:
            book.available = True
            self.list_of_borrowed_books.remove(book)
            print("Книга возвращена!")
        else:
            print("Эта книга не из нашей библиотеки!")

    def show_list(self):
        print(self.list_of_borrowed_books)
