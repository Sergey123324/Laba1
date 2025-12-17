from author import Author

class Book:
    def init(self, author, title, isbn, year):
        self.author = author
        self.title = title
        self.isbn = isbn
        self.year = year
        self.available = True

    def info(self):
        status = "В наличии" if self.available else "Отсутствует"
        return f"Автор:{self.author}, Номер:{self.isbn}, Год выпуска:{self.year}, Статус:{status}"
