class Reader:
    def __init__(self, name, surname, reader_id):
        self.name = name
        self.surname = surname
        self.reader_id = reader_id

    def card(self):
        return f"Читатель: {self.surname} {self.name}, ID: {self.reader_id}"

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "reader_id": self.reader_id
        }