class Album:
    ARTIST_EXCEPTIONS = [ 'BLK', 'BLS', 'BZN', 'BeatKraken',
                      'CHR', 'CLS', 'CPV', 'CQD', 'DCP', 'DG', 'DJ', 'DLux', 'DNI',
                      'DPC', 'DVD', 'DVTZ', 'DaCream', 'DobleJota', 'EP', 'EUPMC',
                      'ElSucio', 'FBeats', 'FJ Ramos', 'FK Crew', 'Ferran MDE',
                      'GT Castellano', 'GranPurismo', 'HC', 'HDC', 'HR', 'IFE',
                      'JHT', 'JML', 'JNK', 'JP', 'JPelirrojo', 'JotaJota', 'KAOS',
                      'KFS & Ochoa', 'LG', 'LJDA', 'LP', 'LSK', 'LaFé', 'LaOdysea',
                      'MC', 'MCB', 'MDE', 'NH', 'NeOne', 'NomadaSquaD',
                      'NonDuermas', 'Nora LaRock', 'PFG', 'PGP', 'RCA', 'RNE3',
                      'RdM', 'SDJ', 'SDave', 'SFDK', 'SH', 'SHN', 'SKL69', 'Sr',
                      'Sr.', 'TCap', 'TDK', 'THX', 'TNGHT', 'TV', 'URS', 'VPS',
                      'VSK', 'VV.AA.', 'XChent', 'XL', 'XXL', 'XXX', 'ZNP', 'vs',
                      'yOSEguiré']

    TITLE_EXCEPTIONS = [
        'BBoy', 'BCM',
        'CD',
    ]
    def __init__(self, artist: str, title: str, publication_date: str, album_format: str):
        self.artist = self._capitalize_artist(artist),
        self.title = self._capitalize_title(title),
        self.publication_date = publication_date,
        self.format = album_format

    def _capitalize_artist(self, name) -> str:
        return name

    def _capitalize_title(self, title) -> str:
        return title
