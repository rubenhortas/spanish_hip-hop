from tools.libraries.config import CSV_SEPARATOR
from tools.libraries.string_utils import replace_exceptions, replace_volumes


class Album:
    _ARTIST_SEPARATORS = [' – ', ' & ', ' Y ', ' X ', ' + ', ' Vs ', ' Vs. ', '-N-', '(', ')']

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

    def get_artists(self) -> list:
        artists = self.artist
        artists = artists.replace('(', '@')
        artists = artists.replace(')', '@')

        for separator in self._ARTIST_SEPARATORS:
            artists = artists.replace(separator, '@')

        return artists.split('@')

    def _format_artist(self, artist: str) -> None:
        self.artist = artist.strip().title()
        self.artist = replace_exceptions(self.artist)
        self.artist = replace_volumes(self.artist)

    def _format_title(self, title: str) -> None:
        self.title = title.strip().capitalize()
        self.title = replace_exceptions(self.title)
        self.title = replace_volumes(self.title)
