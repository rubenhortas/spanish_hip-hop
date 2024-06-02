from collections import Counter

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_HEADER = 'Artista,Trabajo,Fecha Publicación,Tipo'
CSV_SEPARATOR = ','
SEPARATOR_NUMBER = Counter(CSV_HEADER)[CSV_SEPARATOR]
