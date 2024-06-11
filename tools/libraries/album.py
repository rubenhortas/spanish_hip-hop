from tools.libraries.artists import ARTIST_SEPARATORS
from tools.libraries.config import CSV_SEPARATOR, CsvPosition
from tools.libraries.string_utils import has_correct_number_separators, replace_exceptions, fix_volumes, \
    fix_mismatched_square_brackets, fix_mismatched_parentheses


class ExtraSeparatorsException(Exception):
    pass


class Album:
    # FORMATS = ['Directo', 'Doble LP', 'EP', 'LP', 'Maqueta', 'Maxi Single', 'Mixtape', 'Promo', 'Recopilatorio',
    #            'Single']

    def __init__(self, line: str):
        if has_correct_number_separators(line):
            values = line.split(CSV_SEPARATOR)

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

            if not self._has_preserver():
                self._fix_values()
        else:
            raise ExtraSeparatorsException

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

    def get_artists(self) -> list:
        artists = self.artist

        for separator in ARTIST_SEPARATORS:
            artists = artists.replace(separator, '@')

        return artists.split('@')

    def _has_preserver(self) -> bool:
        return self.preserver != ''

    def _get_value(self, string: str) -> str:
        if string and string != '-':
            return string.strip()

        return ''

    def _fix_values(self):
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

    def _format_title(self) -> None:
        self.title = self.title.capitalize()
        self.title = self._fix(self.title)

    def _fix(self, string: str) -> str:
        string_ = fix_mismatched_square_brackets(string)
        string_ = fix_mismatched_parentheses(string_)
        string_ = fix_volumes(string_)
        string_ = replace_exceptions(string_)

        return string_
