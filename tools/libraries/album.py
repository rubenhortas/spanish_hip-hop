from tools.libraries.config import CSV_SEPARATOR
from tools.libraries.string_utils import has_correct_number_separators, replace_exceptions, fix_volumes, \
    fix_mismatched_square_brackets, fix_mismatched_parentheses


class ExtraSeparatorsException(Exception):
    pass


class Album:
    FORMATS = ['Single', 'EP', 'LP', 'Doble LP', 'Mixtape']
    _ARTIST_SEPARATORS = [' – ', ' & ', ' Y ', ' X ', ' + ', ' Vs ', ' Vs. ', '-N-', '(', ')']

    def __init__(self, line: str):
        if has_correct_number_separators(line):
            fields = line.split(CSV_SEPARATOR)

            self.id = self._get_value(fields[0])  # referencia
            self.artist = self._get_value(fields[1])  # artista
            self.title = self._get_value(fields[2])  # trabajo
            self.publication_date = self._get_value(fields[3])  # fecha publicación
            self.format = self._get_value(fields[4])  # tipo
            self.medium = self._get_value(fields[5])  # medio
            self.preserved_in_digital = self._get_value(fields[6])  # preservado en digital
            self.digital_format = self._get_value(fields[7])  # formato digital
            self.bit_rate = self._get_value(fields[8])  # bit rate
            self.preserver = self._get_value(fields[9])  # preservado por
            self.preservation_date = self._get_value(fields[10])  # fecha preservado
            self.modification_date = self._get_value(fields[11])  # fecha modidifcado
            self.source = self._get_value(fields[12])  # fuente
            self.seen_online = self._get_value(fields[13])  # visto online
            self.notes = self._get_value(fields[14])  # notas

            if not self._has_preserver():
                self._fix_fields()
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

        for separator in self._ARTIST_SEPARATORS:
            artists = artists.replace(separator, '@')

        return artists.split('@')

    def _has_preserver(self) -> bool:
        return self.preserver != '' and self.preserver != '-'

    def _get_value(self, string: str) -> str:
        if string and string != '-':
            return string.strip()

        return ''

    def _fix_fields(self):
        self._format_artist()  # artista
        self._format_title()  # trabajo
        self.format = self.format.upper()  # tipo
        self.medium = self.medium.upper()  # medio
        self.preserved_in_digital = self.preserved_in_digital.title()  # preservado en digital
        self.digital_format = self.digital_format.upper()  # formato digital
        self.seen_online = self.seen_online.title()  # visto online

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
