

class Reader:
    def init(self, name, surname, reader_id):
        self.name = name
        self.surname = surname
        self.reader_id = reader_id

    def card(self):
        return (f"Полное имя:{self.name} {self.surname}"
                f"Личный id:{self.reader.id}")

