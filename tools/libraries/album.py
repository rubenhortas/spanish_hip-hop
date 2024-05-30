from tools.libraries.config import CSV_SEPARATOR
from tools.exceptions import EXCEPTIONS


class Album:
    def __init__(self, artist: str, title: str, publication_date: str, album_format: str):
        self.artist = self._format(artist)
        self.title = self._format(title)
        self.publication_date = publication_date.strip()
        self.format = album_format.strip().upper()

    def __str__(self):
        return f"{self.artist}{CSV_SEPARATOR}{self.title}{CSV_SEPARATOR}{self.publication_date}{CSV_SEPARATOR}{self.format}"

    def __eq__(self, other):
        return self.artist == other.artist and self.publication_date == other.publication_date and self.title == other.title and self.format == other.format

    def __lt__(self, other):
        return self.artist < other.artist and self.publication_date < other.publication_date and self.title < other.title and self.format < other.format

    def __gt__(self, other):
        return self.artist > other.artist and self.publication_date > other.publication_date and self.title > other.title and self.format > other.format

    def _format(self, string: str) -> str:
        result = string.strip().capitalize()
        string_ = result.split()

        for word in string_:
            if word.lower() in EXCEPTIONS:
                result = result.replace(word, EXCEPTIONS[word.lower()])

        return result
