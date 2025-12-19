import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
from datetime import datetime


class XMLHandler:
    @staticmethod
    def save_library_data(library, filename="library_data.xml"):
        try:
            root = ET.Element("library")

            metadata = ET.SubElement(root, "metadata")
            ET.SubElement(metadata, "export_date").text = datetime.now().isoformat()
            ET.SubElement(metadata, "total_books").text = str(len(library.books))
            ET.SubElement(metadata, "total_readers").text = str(len(library.readers))
            ET.SubElement(metadata, "version").text = "1.0"

            books_elem = ET.SubElement(root, "books")
            for book in library.books:
                book_elem = ET.SubElement(books_elem, "book")
                ET.SubElement(book_elem, "title").text = book.title
                ET.SubElement(book_elem, "isbn").text = book.isbn
                ET.SubElement(book_elem, "year").text = str(book.year)
                ET.SubElement(book_elem, "available").text = str(book.available).lower()

                author_elem = ET.SubElement(book_elem, "author")
                ET.SubElement(author_elem, "name").text = book.author.name
                ET.SubElement(author_elem, "country").text = book.author.country

            readers_elem = ET.SubElement(root, "readers")
            for reader in library.readers:
                reader_elem = ET.SubElement(readers_elem, "reader")
                ET.SubElement(reader_elem, "name").text = reader.name
                ET.SubElement(reader_elem, "surname").text = reader.surname
                ET.SubElement(reader_elem, "reader_id").text = reader.reader_id

            cards_elem = ET.SubElement(root, "library_cards")
            for card in library.cards:
                card_elem = ET.SubElement(cards_elem, "library_card")

                reader_elem = ET.SubElement(card_elem, "reader")
                ET.SubElement(reader_elem, "reader_id").text = card.reader.reader_id

                borrowed_books_elem = ET.SubElement(card_elem, "borrowed_books")
                for book in card.borrowed_books:
                    book_ref_elem = ET.SubElement(borrowed_books_elem, "book_reference")
                    ET.SubElement(book_ref_elem, "isbn").text = book.isbn
                    ET.SubElement(book_ref_elem, "title").text = book.title

            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(xml_str)

            print(f"Данные успешно сохранены в {filename}")
            return True

        except PermissionError:
            print("Ошибка: нет прав для записи файла")
            return False
        except Exception as e:
            print(f"Ошибка при сохранении в XML: {e}")
            return False

    @staticmethod
    def load_library_data(library, filename="library_data.xml"):
        try:
            if not os.path.exists(filename):
                print(f"Файл {filename} не найден")
                return False

            tree = ET.parse(filename)
            root = tree.getroot()

            library.books.clear()
            library.readers.clear()
            library.cards.clear()

            from author import Author
            from book import Book

            books_elem = root.find("books")
            if books_elem is not None:
                for book_elem in books_elem.findall("book"):
                    title = book_elem.find("title").text
                    isbn = book_elem.find("isbn").text
                    year = int(book_elem.find("year").text)
                    available = book_elem.find("available").text.lower() == "true"

                    author_elem = book_elem.find("author")
                    author_name = author_elem.find("name").text
                    author_country = author_elem.find("country").text

                    author = Author(author_name, author_country)
                    book = Book(title, author, isbn, year)
                    book.available = available
                    library.books.append(book)

            from reader import Reader
            from librarycard import LibraryCard

            readers_elem = root.find("readers")
            if readers_elem is not None:
                for reader_elem in readers_elem.findall("reader"):
                    name = reader_elem.find("name").text
                    surname = reader_elem.find("surname").text
                    reader_id = reader_elem.find("reader_id").text

                    reader = Reader(name, surname, reader_id)
                    library.readers.append(reader)

            cards_elem = root.find("library_cards")
            if cards_elem is not None:
                for card_elem in cards_elem.findall("library_card"):
                    reader_id_elem = card_elem.find("reader/reader_id")
                    if reader_id_elem is not None:
                        reader_id = reader_id_elem.text

                        reader = None
                        for r in library.readers:
                            if r.reader_id == reader_id:
                                reader = r
                                break

                        if reader:
                            card = LibraryCard(reader)

                            borrowed_books_elem = card_elem.find("borrowed_books")
                            if borrowed_books_elem is not None:
                                for book_ref_elem in borrowed_books_elem.findall("book_reference"):
                                    isbn = book_ref_elem.find("isbn").text

                                    for book in library.books:
                                        if book.isbn == isbn:
                                            card.borrowed_books.append(book)
                                            book.available = False
                                            break

                            library.cards.append(card)

            print(f"Данные успешно загружены из {filename}")
            print(f"Загружено: {len(library.books)} книг, {len(library.readers)} читателей")
            return True

        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return False
        except ET.ParseError:
            print(f"Ошибка: файл {filename} содержит некорректный XML")
            return False
        except Exception as e:
            print(f"Ошибка при загрузке из XML: {e}")
            return False