from tools.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_SEPARATOR


def _capitalize(string: str):
    """
    Capitalizes the first letter.
    """
    if string:
        words = string.split()
        first_word = words[0]

        if first_word not in EXCEPTIONS:
            return string[0].upper() + string[1:]

    return string


class Album:
    def __init__(self, line: str):
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

    def _has_preserver(self) -> bool:
        return self.preserver != '' and self.preserver != '-'

    def _format(self):
        self.id = self.id.strip()  # referencia
        self.artist = _capitalize(self.artist.strip())  # artista
        self.title = _capitalize(self.title.strip())  # trabajo
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
