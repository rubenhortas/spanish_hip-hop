#!/usr/bin/env python3

EXCEPTIONS = {
    'a.m.e.n.': 'A.M.E.N.',
    'agosto': 'Agosto',
    'aka': 'AKA',
    'akr': 'AKR',
    'az': 'AZ',
    'B.d.t.r.a.s.h': 'B.D.T.R.A.S.H',
    'B.o.b': 'B.O.B',
    'B.r.u.t.a.l': 'B.R.U.T.A.L',
    'bboy': 'BBoy',
    'bcm': 'BCM',
    'beatkraken': 'BeatKraken',
    'blk': 'BLK',
    'bls': 'BLS',
    'bob': 'Bob',
    'brian': 'Brian',
    'bso': 'BSO',
    'bxl': 'BXL',
    'bzn': 'BZN',
    'cd': 'CD',
    'ce': 'Ce',
    'chr': 'CHR',
    'clasiko': 'Clasiko',
    'cls': 'CLS',
    'coleta': 'Coleta',
    'cpv': 'CPV',
    'cqd': 'CQD',
    'csk': 'CSK',
    'cts': 'CTS',
    'dacream': 'DaCream',
    'dcp': 'DCP',
    'dg': 'DG',
    'dj': 'DJ',
    'dlux': 'DLux',
    'dni': 'DNI',
    'dnoe': 'Dnoe',
    'doblejota': 'DobleJota',
    'dpc': 'DPC',
    'dvd': 'DVD',
    'dvtz': 'DVTZ',
    'e-d-d-h': 'E-D-D-H',
    'elsucio': 'ElSucio',
    'elvis': 'elvis',
    'eme': 'Eme',
    'ep': 'EP',
    'eupmc': 'EUPMC',
    'fbeats': 'FBeats',
    'ferran Mde': 'Ferran MDE',
    'fj Ramos': 'FJ Ramos',
    'fk Crew': 'FK Crew',
    'granpurismo': 'GranPurismo',
    'gt Castellano': 'GT Castellano',
    'hc': 'HC',
    'hdc': 'HDC',
    'hdv': 'JDV',
    'heron': 'Heron',
    'hht': 'JHT',
    'hml': 'JML',
    'hnk': 'JNK',
    'hotajota': 'JotaJota',
    'hp': 'JP',
    'hpelirrojo': 'JPelirrojo',
    'hr': 'HR',
    'ife': 'IFE',
    'ii': 'II',
    'juaninacka': 'Juaninacka',
    'kaos': 'KAOS',
    'kfs & Ochoa': 'KFS & Ochoa',
    'kong': 'Kong',
    'kuze': 'Kuze',
    'lafé': 'LaFé',
    'laodysea': 'LaOdysea',
    'lg': 'LG',
    'ljda': 'LJDA',
    'lp': 'LP',
    'lsk': 'LSK',
    'marley': 'Marley',
    'mc': 'MC',
    'mc\'s': 'MC\'s',
    'mcb': 'MCB',
    'mde': 'MDE',
    'minaj': 'Minaj',
    'mm': 'mm',
    'neone': 'NeOne',
    'nh': 'NH',
    'nicki': 'Nicki',
    'nomadasquad': 'NomadaSquaD',
    'nonduermas': 'NonDuermas',
    'nora Larock': 'Nora LaRock',
    'pfg': 'PFG',
    'pgp': 'PGP',
    'r.p.m': 'R.P.M',
    'rca': 'RCA',
    'rdm': 'RdM',
    'rne3': 'RNE3',
    'scott': 'Scott',
    'sdave': 'SDave',
    'sdj': 'SDJ',
    'sfdk': 'SFDK',
    'sh': 'SH',
    'shn': 'SHN',
    'skl69': 'SKL69',
    'sr': 'Sr',
    'sr.': 'Sr.',
    'tb': 'TB',
    'tcap': 'TCap',
    'tdk': 'TDK',
    'thx': 'THX',
    'tnght': 'TNGHT',
    'torne': 'Torne',
    'tv': 'TV',
    'urs': 'URS',
    'uve': 'Uve',
    'vol.': 'Vol.',
    'vps': 'VPS',
    'vs': 'vs',
    'vsk': 'VSK',
    'vv.Aa.': 'VV.AA.',
    'w.o.l.': 'W.O.L.',
    'x': 'V',
    'xchent': 'XChent',
    'Xl': 'XL',
    'xl': 'XL',
    'xxl': 'XXL',
    'xxx': 'XXX',
    'yoseguiré': 'yOSEguiré',
    'znp': 'ZNP',
}

if __name__ == '__main__':
    """
    Print dictionary entries in alphabetical order
    """
    try:
        file_name = 'sorted_dictionary.txt'
        unique_keys = []
        result = []

        for key in EXCEPTIONS:
            if key not in unique_keys:
                unique_keys.append(key)

        for key in sorted(unique_keys, key=str.casefold):
            key_ = key.replace("'", "\\'")
            value = EXCEPTIONS[key].replace("'", "\\'")
            result.append(f"'{key_}': '{value}',\n")

        with open(file_name, 'w') as f:
            f.writelines(result)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{file_name}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file_name}' OSError: {os_error}")
        exit(-1)
