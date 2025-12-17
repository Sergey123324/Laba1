class Author:

    def init(self, name, country):
        self.name = name
        self.country = country

    def info(self):
        return f"{self.name} ({self.country})"