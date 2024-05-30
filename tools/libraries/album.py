from tools.libraries.config import CSV_SEPARATOR
from tools.exceptions import EXCEPTIONS


class Album:
    def __init__(self, artist: str, title: str, publication_date: str, album_format: str):
        self._format_artist(artist)
        self._format_title(title)
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

    def _format_artist(self, artist) -> None:
        self.artist = artist.strip().title()
        artist_ = self.artist.split()

        for word in artist_:
            if word.lower() in EXCEPTIONS:
                self.artist = self.artist.replace(word, EXCEPTIONS[word.lower()])

    def _format_title(self, title) -> None:
        self.title = title.strip().capitalize()
        title_ = self.title.split()

        for word in title_:
            if word.lower() in EXCEPTIONS:
                self.title = self.title.replace(word, EXCEPTIONS[word.lower()])
