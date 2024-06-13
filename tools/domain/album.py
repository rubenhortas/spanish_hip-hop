from tools.config.config import CSV_SEPARATOR, CsvPosition
from tools.utils.string_utils import has_correct_number_separators, replace_exceptions, fix_volumes, \
    fix_mismatched_square_brackets, fix_mismatched_parentheses


class WrongSeparatorsException(Exception):
    pass


class Album:
    def __init__(self, line: str):
        if has_correct_number_separators(line):
            values = line.split(CSV_SEPARATOR)

            # CSV values
            self.id = self._get_value(values[CsvPosition.ID.value])
            self.artist = self._get_value(values[CsvPosition.ARTIST.value])
            self.title = self._get_value(values[CsvPosition.TITLE.value])
            self.publication_date = self._get_value(values[CsvPosition.PUBLICATION_DATE.value])
            self.format = self._get_value(values[CsvPosition.FORMAT.value])
            self.medium = self._get_value(values[CsvPosition.MEDIUM.value])
            self.preserved_in_digital = self._get_value(values[CsvPosition.PRESERVED_IN_DIGITAL.value])
            self.digital_format = self._get_value(values[CsvPosition.DIGITAL_FORMAT.value])
            self.bit_rate = self._get_value(values[CsvPosition.BIT_RATE.value])
            self.preserver = self._get_value(values[CsvPosition.PRESERVER.value])
            self.preservation_date = self._get_value(values[CsvPosition.PRESERVATION_DATE.value])
            self.modification_date = self._get_value(values[CsvPosition.MODIFICATION_DATE.value])
            self.source = self._get_value(values[CsvPosition.SOURCE.value])
            self.seen_online = self._get_value(values[CsvPosition.SEEN_ONLINE.value])
            self.notes = self._get_value(values[CsvPosition.NOTES.value])

            # Not CSV values
            self._artists_separators = []
            self._artists = []

            if not self.has_preserver():
                self._format_values()
        else:
            raise WrongSeparatorsException

    def __str__(self):
        return (f"{self.id}{CSV_SEPARATOR}"
                f"{self.artist}{CSV_SEPARATOR}"
                f"{self.title}{CSV_SEPARATOR}"
                f"{self.publication_date}{CSV_SEPARATOR}"
                f"{self.format}{CSV_SEPARATOR}"
                f"{self.medium}{CSV_SEPARATOR}"
                f"{self.preserved_in_digital}{CSV_SEPARATOR}"
                f"{self.digital_format}{CSV_SEPARATOR}"
                f"{self.bit_rate}{CSV_SEPARATOR}"
                f"{self.preserver}{CSV_SEPARATOR}"
                f"{self.preservation_date}{CSV_SEPARATOR}"
                f"{self.modification_date}{CSV_SEPARATOR}"
                f"{self.source}{CSV_SEPARATOR}"
                f"{self.seen_online}{CSV_SEPARATOR}"
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

    def has_preserver(self) -> bool:
        return self.preserver != ''

    def get_artists(self) -> list:
        if not self._artists:
            if not self._artists_separators:
                self.get_artist_separators()

            album_artist = self.artist
            album_artist = album_artist.replace('(', '').replace(')', '')
            album_artist = album_artist.replace('[', '').replace(']', '')

            for separator in self._artists_separators:
                album_artist = album_artist.replace(separator, '|')

            artists_ = album_artist.split('|')

            for artist in artists_:
                artist_ = artist.strip()

                if artist_:
                    self._artists.append(artist_)
                    
        return self._artists

    def get_artist_separators(self) -> list:
        if not self._artists_separators:
            separators = []
            words = self.artist.split()

            for word in words:
                if len(word) == 1 and (word.lower() == 'y' or not word.isalnum()):
                    separators.append(word)

            self._artists_separators = separators

        return self._artists_separators

    def _get_value(self, string: str) -> str:
        if string and string != '-':
            return string.strip()

        return ''

    def _format_values(self):
        self._format_artist()
        self._format_title()
        self.format = self.format.upper()
        self.medium = self.medium.upper()
        self.preserved_in_digital = self.preserved_in_digital.capitalize()
        self.bit_rate = self.bit_rate.upper()
        self.digital_format = self.digital_format.upper()
        self.seen_online = self.seen_online.capitalize()

    def _format_artist(self) -> None:
        self.artist = self.artist.title()
        self.artist = self._fix(self.artist)
        self.artist = replace_exceptions(self.artist)

    def _format_title(self) -> None:
        self.title = self.title.capitalize()
        self.title = self._fix(self.title)
        self.title = replace_exceptions(self.title)

    def _fix(self, string: str) -> str:
        string_ = string.replace('"', '')
        string_ = fix_mismatched_square_brackets(string_)
        string_ = fix_mismatched_parentheses(string_)
        string_ = fix_volumes(string_)

        return string_
