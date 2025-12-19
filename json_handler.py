import json
import os
from datetime import datetime


class JSONHandler:
    @staticmethod
    def save_library_data(library, filename="library_data.json"):
        try:
            data = library.to_dict()

            data["metadata"] = {
                "export_date": datetime.now().isoformat(),
                "total_books": len(library.books),
                "total_readers": len(library.readers),
                "version": "1.0"
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            print(f"Данные успешно сохранены в {filename}")
            return True

        except PermissionError:
            print("Ошибка: нет прав для записи файла")
            return False
        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")
            return False

    @staticmethod
    def load_library_data(library, filename="library_data.json"):
        try:
            if not os.path.exists(filename):
                print(f"Файл {filename} не найден")
                return False

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            library.books.clear()
            library.readers.clear()
            library.cards.clear()

            from author import Author
            from book import Book

            for book_data in data.get("books", []):
                author_data = book_data.get("author", {})
                author = Author(author_data.get("name", ""),
                                author_data.get("country", ""))
                book = Book(book_data.get("title", ""),
                            author,
                            book_data.get("isbn", ""),
                            book_data.get("year", 0))
                book.available = book_data.get("available", True)
                library.books.append(book)

            from reader import Reader
            from librarycard import LibraryCard

            for reader_data in data.get("readers", []):
                reader = Reader(reader_data.get("name", ""),
                                reader_data.get("surname", ""),
                                reader_data.get("reader_id", ""))
                library.readers.append(reader)

                card = LibraryCard(reader)

                for card_data in data.get("library_cards", []):
                    if card_data["reader"]["reader_id"] == reader.reader_id:
                        for book_dict in card_data.get("borrowed_books", []):
                            for book in library.books:
                                if book.isbn == book_dict.get("isbn"):
                                    card.borrowed_books.append(book)
                                    book.available = False

                library.cards.append(card)

            print(f"Данные успешно загружены из {filename}")
            print(f"Загружено: {len(library.books)} книг, {len(library.readers)} читателей")
            return True

        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return False
        except json.JSONDecodeError:
            print(f"Ошибка: файл {filename} содержит некорректный JSON")
            return False
        except Exception as e:
            print(f"Ошибка при загрузке из JSON: {e}")
            return False