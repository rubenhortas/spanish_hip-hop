from tools.config.config import CSV_DELIMITER, CsvPosition
from tools.utils.string_utils import replace_exceptions, fix_volumes, fix_mismatched_square_brackets, fix_mismatched_parentheses


class WrongFieldsNumberException(Exception):
    pass


class Album:
    @property
    def artists(self):
        return Album.get_artists(self.artist)

    def __init__(self, line: str, fields_number: int):
        if len(line) == fields_number:
            # CSV values
            self.id = self._get_value(line[CsvPosition.ID.value])
            self.artist = self._get_value(line[CsvPosition.ARTIST.value])
            self.title = self._get_value(line[CsvPosition.TITLE.value])
            self.publication_date = self._get_value(line[CsvPosition.PUBLICATION_DATE.value])
            self.format = self._get_value(line[CsvPosition.FORMAT.value])
            self.medium = self._get_value(line[CsvPosition.MEDIUM.value])
            self.preserved_in_digital = self._get_value(line[CsvPosition.PRESERVED_IN_DIGITAL.value])
            self.digital_format = self._get_value(line[CsvPosition.DIGITAL_FORMAT.value])
            self.bit_rate = self._get_value(line[CsvPosition.BIT_RATE.value])
            self.preserver = self._get_value(line[CsvPosition.PRESERVER.value])
            self.preservation_date = self._get_value(line[CsvPosition.PRESERVATION_DATE.value])
            self.modification_date = self._get_value(line[CsvPosition.MODIFICATION_DATE.value])
            self.source = self._get_value(line[CsvPosition.SOURCE.value])
            self.seen_online = self._get_value(line[CsvPosition.SEEN_ONLINE.value])
            self.notes = self._get_value(line[CsvPosition.NOTES.value])

            if not self.has_preserver():
                self._format_values()
        else:
            raise WrongFieldsNumberException

    def __str__(self):
        return (f"{self.id}{CSV_DELIMITER}"
                f"{self.artist}{CSV_DELIMITER}"
                f"{self.title}{CSV_DELIMITER}"
                f"{self.publication_date}{CSV_DELIMITER}"
                f"{self.format}{CSV_DELIMITER}"
                f"{self.medium}{CSV_DELIMITER}"
                f"{self.preserved_in_digital}{CSV_DELIMITER}"
                f"{self.digital_format}{CSV_DELIMITER}"
                f"{self.bit_rate}{CSV_DELIMITER}"
                f"{self.preserver}{CSV_DELIMITER}"
                f"{self.preservation_date}{CSV_DELIMITER}"
                f"{self.modification_date}{CSV_DELIMITER}"
                f"{self.source}{CSV_DELIMITER}"
                f"{self.seen_online}{CSV_DELIMITER}"
                f"{self.notes}")

    def __eq__(self, other):
        return (self.id == other.id
                and self.artist == other.artist
                and self.title == other.title
                and self.publication_date == other.publication_date
                and self.format == other.format
                and self.medium == other.medium
                and self.preserved_in_digital == other.preserved_in_digital
                and self.digital_format == other.digital_format
                and self.bit_rate == other.bit_rate
                and self.preserver == other.preserver
                and self.preservation_date == other.preservation_date
                and self.modification_date == other.modification_date
                and self.source == other.source
                and self.seen_online == other.seen_online
                and self.notes == other.notes)

    def __lt__(self, other):
        return (self.id < other.id
                and self.artist < other.artist
                and self.publication_date < other.publication_date
                and self.title < other.title
                and self.format < other.format
                and self.medium < other.medium
                and self.preserved_in_digital < other.preserved_in_digital
                and self.digital_format < other.digital_format
                and self.bit_rate < other.bit_rate
                and self.preserver < other.preserver
                and self.preservation_date < other.preservation_date
                and self.modification_date < other.modification_date
                and self.source < other.source
                and self.seen_online < other.seen_online
                and self.notes < other.notes)

    def __gt__(self, other):
        return (self.id > other.id
                and self.artist > other.artist
                and self.publication_date > other.publication_date
                and self.title > other.title
                and self.format > other.format
                and self.medium > other.medium
                and self.preserved_in_digital > other.preserved_in_digital
                and self.digital_format > other.digital_format
                and self.bit_rate > other.bit_rate
                and self.preserver > other.preserver
                and self.preservation_date > other.preservation_date
                and self.modification_date > other.modification_date
                and self.source > other.source
                and self.seen_online > other.seen_online
                and self.notes > other.notes)

    @staticmethod
    def format_artist(artist: str) -> str:
        artist_ = artist.title()
        artist_ = Album._fix(artist_)
        artist_ = replace_exceptions(artist_)

        return artist_

    @staticmethod
    def get_artists(artist: str) -> (list, list):
        artists = []
        separators = Album._get_separators(artist)

        album_artist = artist
        album_artist = album_artist.replace('(', '').replace(')', '')
        album_artist = album_artist.replace('[', '').replace(']', '')

        for separator in separators:
            album_artist = album_artist.replace(f" {separator}", '|')

        album_artists = album_artist.split('|')

        for artist in album_artists:
            artist_ = artist.strip()

            if artist_:
                artists.append(artist_)

        return artists, separators

    def list(self) -> list:
        return [self.id,
                self.artist,
                self.title,
                self.publication_date,
                self.format,
                self.medium,
                self.preserved_in_digital,
                self.digital_format,
                self.bit_rate,
                self.preserver,
                self.preservation_date,
                self.modification_date,
                self.source,
                self.seen_online,
                self.notes]

    def has_preserver(self) -> bool:
        return self.preserver != ''

    @staticmethod
    def _get_separators(artist: str) -> list:
        separators = []
        artists = artist.split()

        for word in artists:
            if len(word) == 1 and (word.lower() == 'y' or not word.isalnum()):
                separators.append(word)

        return separators

    @staticmethod
    def _get_value(string: str) -> str:
        if string and string != '-':
            return string.strip()

        return ''

    @staticmethod
    def _fix(string: str) -> str:
        string_ = fix_mismatched_square_brackets(string)
        string_ = fix_mismatched_parentheses(string_)
        string_ = fix_volumes(string_)

        return string_

    def _format_values(self):
        self.artist = Album.format_artist(self.artist)
        self._format_title()
        self.format = self.format.upper()
        self.medium = self.medium.upper()
        self.preserved_in_digital = self.preserved_in_digital.capitalize()
        self.bit_rate = self.bit_rate.upper()
        self.digital_format = self.digital_format.upper()
        self.seen_online = self.seen_online.capitalize()

    def _format_title(self) -> None:
        self.title = self.title.capitalize()
        self.title = self._fix(self.title)
        self.title = replace_exceptions(self.title)
