import Artist, Title


class Album:
    artist_exceptions = Artist.EXCEPTIONS
    title_exceptions = Title.EXCEPTIONS

    def __init__(self, artist: str, title: str, publication_date: str, album_format: str, csv_separator: str):
        self._format_artist(artist)
        self._format_title(title)
        self.publication_date = publication_date
        self.format = album_format
        self.csv_separator = csv_separator

    def __str__(self):
        return f"{self.artist}{self.csv_separator}{self.title}{self.csv_separator}{self.publication_date}{self.csv_separator}{self.format}"

    def list(self):
        return [self.artist, self.title, self.publication_date, self.format]

    def _format_artist(self, artist: str) -> None:
        self.artist = artist.title()

        for word in self.artist:
            if word in self.artist_exceptions:
                self.artist.replace(word, self.artist_exceptions[word])

    def _format_title(self, title: str) -> None:
        self.title = title.capitalize()

        for word in self.title:
            if word in self.title_exceptions:
                self.title.replace(word, self.title_exceptions[word])
