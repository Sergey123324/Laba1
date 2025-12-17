class Author:
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def info(self):
        return f"{self.name} ({self.country})"

    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country
        }