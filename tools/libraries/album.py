from collections import Counter

from tools.libraries.config import CSV_SEPARATOR, SEPARATOR_NUMBER
from tools.libraries.string_utils import replace_exceptions, replace_volumes


def _has_correct_number_separators(line: str) -> bool:
    return Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER


class Album:
    FORMATS = ['Single', 'EP', 'LP', 'Doble LP', 'Mixtape']
    _ARTIST_SEPARATORS = [' – ', ' & ', ' Y ', ' X ', ' + ', ' Vs ', ' Vs. ', '-N-', '(', ')']

    def __init__(self, line: str):
        if _has_correct_number_separators(line):
            fields = line.split(CSV_SEPARATOR)

            self.id = fields[0]  # referencia
            self.artist = fields[1].strip()  # artista
            self.title = fields[2].strip()  # trabajo
            self.publication_date = fields[3]  # fecha publicación
            self.format = fields[4].capitalize()  # tipo
            self.medium = fields[5].upper()  # medio
            self.preserved_in_digital = fields[6].title()  # preservado en digital
            self.digital_format = fields[7].upper()  # formato digital
            self.bit_rate = fields[8]  # bit rate
            self.preserver = fields[9]  # preservado por
            self.preservation_date = fields[10]  # fecha preservado
            self.modification_date = fields[11]  # fecha modidifcado
            self.source = fields[12]  # fuente
            self.seen_online = fields[13].title()  # visto online
            self.notes = fields[14]  # notas

            if not self._has_preserver():
                self._format()
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
        artists = artists.replace('(', '@')
        artists = artists.replace(')', '@')

        for separator in self._ARTIST_SEPARATORS:
            artists = artists.replace(separator, '@')

        return artists.split('@')

    def _has_preserver(self) -> bool:
        return self.preserver != '' and self.preserver != '-'

    def _format(self):
        self.id = self.id.strip()  # referencia
        self._format_artist()  # artista
        self._format_title()  # trabajo
        self.publication_date = self.publication_date.strip()  # fecha publicación
        self.format = self.format.strip().capitalize()  # tipo
        self.medium = self.medium.strip().upper()  # medio
        self.preserved_in_digital = self.preserved_in_digital.strip().title()  # preservado en digital
        self.digital_format = self.digital_format.strip().upper()  # formato digital
        self.bit_rate = self.bit_rate.strip()  # bit rate
        self.preserver = self.preserver.strip()  # preservado por
        self.preservation_date = self.preservation_date.strip()  # fecha preservado
        self.modification_date = self.modification_date.strip()  # fecha modidifcado
        self.source = self.source.strip()  # fuente
        self.seen_online = self.seen_online.strip().title()  # visto online
        self.notes = self.notes.strip()  # notas

    def _format_artist(self) -> None:
        self.artist = self.artist.strip().title()
        self.artist = replace_exceptions(self.artist)
        self.artist = replace_volumes(self.artist)

    def _format_title(self) -> None:
        self.title = self.title.strip().capitalize()
        self.title = replace_exceptions(self.title)
        self.title = replace_volumes(self.title)


class ExtraSeparatorsException(Exception):
    pass
