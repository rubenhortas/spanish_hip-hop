from collections import Counter

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_HEADER = 'Referencia,Artista,Trabajo,"Fecha Publicación",Tipo,Medio,"Preservado en digital","Formato digital",Bitrate,"Preservado por","Fecha preservado","Fecha modificado",Fuente,"Visto online",Notas'
CSV_SEPARATOR = ','
SEPARATOR_NUMBER = Counter(CSV_HEADER)[CSV_SEPARATOR]
