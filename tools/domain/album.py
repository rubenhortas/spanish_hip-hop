from tools.config.config import CSV_SEPARATOR, CsvPosition
from tools.utils.string_utils import has_correct_number_separators, replace_exceptions, fix_volumes, \
    fix_mismatched_square_brackets, fix_mismatched_parentheses


class WrongSeparatorsException(Exception):
    pass


class Album:
    @property
    def artists(self):
        return Album.get_artists(self.artist)
    
    def __init__(self, line: str):
        if has_correct_number_separators(line):
            values = line.split(CSV_SEPARATOR)

            # CSV values
            self.id = self._get_value(values[CsvPosition.ID.value])
            self.artist = self._get_value(values[CsvPosition.ARTIST.value])
            self.title = self._get_value(values[CsvPosition.TITLE.value])
            self._publication_date = self._get_value(values[CsvPosition.PUBLICATION_DATE.value])
            self._format = self._get_value(values[CsvPosition.FORMAT.value])
            self._medium = self._get_value(values[CsvPosition.MEDIUM.value])
            self._preserved_in_digital = self._get_value(values[CsvPosition.PRESERVED_IN_DIGITAL.value])
            self._digital_format = self._get_value(values[CsvPosition.DIGITAL_FORMAT.value])
            self._bit_rate = self._get_value(values[CsvPosition.BIT_RATE.value])
            self._preserver = self._get_value(values[CsvPosition.PRESERVER.value])
            self._preservation_date = self._get_value(values[CsvPosition.PRESERVATION_DATE.value])
            self._modification_date = self._get_value(values[CsvPosition.MODIFICATION_DATE.value])
            self._source = self._get_value(values[CsvPosition.SOURCE.value])
            self._seen_online = self._get_value(values[CsvPosition.SEEN_ONLINE.value])
            self._notes = self._get_value(values[CsvPosition.NOTES.value])

            if not self.has_preserver():
                self._format_values()
        else:
            raise WrongSeparatorsException

    def __str__(self):
        return (f"{self.id}{CSV_SEPARATOR}"
                f"{self.artist}{CSV_SEPARATOR}"
                f"{self.title}{CSV_SEPARATOR}"
                f"{self._publication_date}{CSV_SEPARATOR}"
                f"{self._format}{CSV_SEPARATOR}"
                f"{self._medium}{CSV_SEPARATOR}"
                f"{self._preserved_in_digital}{CSV_SEPARATOR}"
                f"{self._digital_format}{CSV_SEPARATOR}"
                f"{self._bit_rate}{CSV_SEPARATOR}"
                f"{self._preserver}{CSV_SEPARATOR}"
                f"{self._preservation_date}{CSV_SEPARATOR}"
                f"{self._modification_date}{CSV_SEPARATOR}"
                f"{self._source}{CSV_SEPARATOR}"
                f"{self._seen_online}{CSV_SEPARATOR}"
                f"{self._notes}")

    def __eq__(self, other):
        return (self.id == other.id
                and self.artist == other.artist
                and self.title == other.title
                and self._publication_date == other._publication_date
                and self._format == other._format
                and self._medium == other._medium
                and self._preserved_in_digital == other._preserved_in_digital
                and self._digital_format == other._digital_format
                and self._bit_rate == other._bit_rate
                and self._preserver == other._preserver
                and self._preservation_date == other._preservation_date
                and self._modification_date == other._modification_date
                and self._source == other._source
                and self._seen_online == other._seen_online
                and self._notes == other._notes)

    def __lt__(self, other):
        return (self.id < other.id
                and self.artist < other.artist
                and self._publication_date < other._publication_date
                and self.title < other.title
                and self._format < other._format
                and self._medium < other._medium
                and self._preserved_in_digital < other._preserved_in_digital
                and self._digital_format < other._digital_format
                and self._bit_rate < other._bit_rate
                and self._preserver < other._preserver
                and self._preservation_date < other._preservation_date
                and self._modification_date < other._modification_date
                and self._source < other._source
                and self._seen_online < other._seen_online
                and self._notes < other._notes)

    def __gt__(self, other):
        return (self.id > other.id
                and self.artist > other.artist
                and self._publication_date > other._publication_date
                and self.title > other.title
                and self._format > other._format
                and self._medium > other._medium
                and self._preserved_in_digital > other._preserved_in_digital
                and self._digital_format > other._digital_format
                and self._bit_rate > other._bit_rate
                and self._preserver > other._preserver
                and self._preservation_date > other._preservation_date
                and self._modification_date > other._modification_date
                and self._source > other._source
                and self._seen_online > other._seen_online
                and self._notes > other._notes)

    @staticmethod
    def format_artist(artist: str) -> str:
        artist_ = artist.title()
        artist_ = Album._fix(artist_)
        artist_ = replace_exceptions(artist_)

        return artist_

    @staticmethod
    def get_artists(artist: str) -> list:
        artists = []
        separators = Album._get_separators(artist)

        album_artist = artist
        album_artist = album_artist.replace('(', '').replace(')', '')
        album_artist = album_artist.replace('[', '').replace(']', '')

        for separator in separators:
            album_artist = album_artist.replace(separator, '|')

        album_artists = album_artist.split('|')

        for artist in album_artists:
            artist_ = artist.strip()

            if artist_:
                artists.append(artist_)

        return artists

    def has_preserver(self) -> bool:
        return self._preserver != ''

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
        string_ = string.replace('"', '')
        string_ = fix_mismatched_square_brackets(string_)
        string_ = fix_mismatched_parentheses(string_)
        string_ = fix_volumes(string_)

        return string_

    def _format_values(self):
        self.artist = Album.format_artist(self.artist)
        self._format_title()
        self._format = self._format.upper()
        self._medium = self._medium.upper()
        self._preserved_in_digital = self._preserved_in_digital.capitalize()
        self._bit_rate = self._bit_rate.upper()
        self._digital_format = self._digital_format.upper()
        self._seen_online = self._seen_online.capitalize()

    def _format_title(self) -> None:
        self.title = self.title.capitalize()
        self.title = self._fix(self.title)
        self.title = replace_exceptions(self.title)
