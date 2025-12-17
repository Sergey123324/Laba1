from author import Author


class Book:
    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True

    def info(self):
        status = "В наличии" if self.available else "Отсутствует"
        return f"'{self.title}' - {self.author.info()}, ISBN: {self.isbn}, Год: {self.year}, Статус: {status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author.to_dict(),
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available
        }