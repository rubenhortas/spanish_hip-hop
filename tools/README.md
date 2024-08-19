#tools

## ¿Qué son estas herramientas?

Estas herramientas son pequeños scripts en python para mantener el  fichero [lista trabajos hip-hop español.csv](https://github.com/ctRl-ES/spanish_hip-hop/edit/master/lista%20trabajos%20hip-hop%20espa%C3%B1ol.csv).

## Cómo consigo el fichero?

Para conseguir una versión actualizada del fichero contacta con [@ctRl](https://github.com/ctRl-ES/).

## ¿Cómo se utilizan estas herramientas?

### Crea un entorno virtual (o venv)

```shell
python3 -m venv shhvenv
```

*Sólo tienes que hacer esto la primera vez*

### Activa el *venv*

* Linux/macOS

```shell
source shhvenv/bin/activate
```

* Windows

```shell
shhvenv\Scripts\activate
```

*Tienes que hacer esto cada vez que lo utilices*

### Instala los requisitos

```shell
source pmvenv/bin/activate
```

*Sólo tienes que hacer esto la primera vez*

### Coloca el el fichero `lista trabajos hip-hop español.csv` en el directorio de los scripts y ejecuta el script escogido.

## ¿Para qué sirven estas herramientas?

### fix_file.py

Soluciona varios errores presentes en el fichero original:

  * Elimina los artistas extranjeros
  * Elimina los dobles espacios en blanco
  * Elimina los "desconocidos" de los campos

Genera los siguientes ficheros de salida:

  * Fichero CSV con las líneas arregladas
  * Fichero CSV con las líneas que tienen un número de campos incorrecto (si las hay)
  * Fichero CSV con los artistas extranjeros (si los hay)

Éste script debe ser utilizado el primero, para poder ejecutar el resto de scripts sobre un fichero arreglado, y sólo deber ser utilizado con la versión original del fichero.

### format_file.py

Formatea el fichero CSV.

Genera los siguientes ficheros de salida:

  * Nuevo fichero CSV formateado
  * Fichero CSV con los errores encontrados (si hay)

Los parámetros del formateo se pueden configurar en el fichero `/config/config.py`, en la sección `## Format config`.
Por defecto (y como opción recomendada) están todas las opciones activadas (True).

### get_duplicates.py

Obtiene las entradas duplicadas (y posiblemente duplicadas) del fichero CSV.
Las entradas posiblemente duplicadas son entradas muy parecidas entre sí que deben ser revisadas.

Genera los siguientes ficheros de salida:

  * Fichero CSV con las entradas duplicadas y con las entradas posiblemente duplicadas (si hay).

### get_issues.py

Busca los siguientes erroes en el fichero CSV:

  * Líneas con número incorrecto de campos
  * Líneas con paréntesis no coincidentes
  * Líneas con corchetes no coincidentes
  * Líneas con comillas no coincidentes
  * Líneas con posible fecha de publicación en el título pero no en su campo correspondiente
  * Líneas con posible formato de álbum en el título pero no en su campo correspondiente

Genera los siguientes ficheros de salida:

  * Fichero CSV con las líneas con número incorrecto de campos (si hay)
  * Fichero CSV con las líneas con paréntesis no coincidentes (si hay)
  * Fichero CSV con las líneas con corchetes no coincidentes (si hay)
  * Fichero CSV con las líneas con comillas no coincidentes (si hay)
  * Fichero CSV con las líneas con posible fecha de publicación en el titulo pero no en su campo correspondiente
  * Fichero CSV con las líneas con posible formato de álbum en el título pero no en su campo correspondiente

### regenerate_artists_dictionary.py

Actualiza el diccionario de traducción de nombres de artistas `ARTISTS`, en el fichero `/config/artists.py`.
Combina los nombres de artistas del diccionario `ARTISTS` con los nombres de artistas de los álbums del fichero CSV.
El diccionario resultante estará libre de duplicados y ordenado alfabéticamente.

### regenerate_exceptions_dictionary.py

Actualiza el diccionario de excepciones `EXCEPTIONS` del fichero `/config/exceptions.py`.
El diccionario resultante estará libre de duplicados y ordenado alfabéticamente.

## Configuración

### config.py

En este fichero se configuran las opciones releativas al fichero CSV, opciones relativas a los álbums y las opciones relativas al formateo.

  * Opciones del fichero CSV:

    * `CSV_FILE`: Nombre del fichero
    * `CSV_HEADER`: Cabecera del fichero
    * `CSV_DELIMITER`: Delimitador
    * `CSV_EMPTY_FIELD_VALUE`: Valor del campo vacío
  
  * Opciones de álbum

    * `ALBUM_FORMATS`: Formatos de álbum

  * Opciones de formateo:

    * `FIX_MISMATCHED_PARENTHESES`: Arreglar paréntesis no concidentes
    * `FIX_MISMATCHED_QUOTES`: Arreglar comillas no coincidentes
    * `FIX_MISMATCHED_SQUARE_BRACKETS`: Arreglar corchetes no coincidentes
    * `FIX_VOLUMES`: Arreglar nombres de volúmenes
    * `CAPITALIZE_ACRONYMS`: Convertir a mayúsculas los acrónimos
    * `REPLACE_ARTISTS_IN_TITLES`: Reemplazar los nombres de artistas en los títulos

### artists.py

Diccionario de traducción de nombres de artista.

Establecer el valor de nombre para un artista sirve para preservar mayúsculas, minúsculas, palabras especiales, etc.   
Por ejemplo: `'alice': 'ALiCe',` hará que cada vez que se encuentre "*alice*" como nombre de artista (ignorando mayúsculas y minúsculas) sea convertido a "*ALiCe*".  
Las excepciones definidas en el diccionario `EXCEPTIONS` del fichero `/config/exceptions.py` no serán aplicadas al formateo de  los nombres de los artistas.

El formato del diccionario `ARTISTS` es `'clave': 'valor'`:

  * 'clave': Nombre del artista en minúsculas
  * 'valor': Nombre al que será transformado el nombre de artista de la clave.
    * El formato por defecto es "titlecase" (la primera letra de cada palabra en mayúsculas), por ejemplo: 'Bob The Foobar'.

```python
ARTISTS = {
    'alice':'ALiCe',  # 'clave': 'valor'
    'bob the foobar': 'Bob The Foobar',
}
```

### exceptions.py

Diccionario de conversión de excepciones de palabras.

Establecer excepciones sirve para conservar mayúsculas, minúsculas, palabras especiales, etc.  
Por ejemplo: `'foobar': 'FooBaR'` hará que cada vez que se encuentre la palabra "*foobar*" (ignorando las mayúsculas y las minúsculas), en el título de un álbum, sea transformada a "*FooBaR*".  
Las excepciones del diccionario `EXCEPTIONS` **NO** serán aplicadas a los transformaciones de los nombres de los artistas.

El formato del diccionario `EXCEPTIONS` es `'clave': 'valor'`:
  * 'clave': La palabra en minúsculas
  * 'valor': El valor al que será transformada la palabra.

```python
EXCEPTIONS = {
    'foo': 'fOo',  # 'clave': 'valor'
    'bar': 'BaR',
}
```

## ¿Cómo puedo colaborar?

* Date de alta en [github](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home)

    * Sube nuevos scripts que aporten nuevas funcionalidades.
    * Corrige errores (o añade nuevas funcionalidades) en los scripts de herramientas.
    * Aporta nuevas herramientas que ayuden a la gestión de este proyecto.

* Echa un ojo a los [Issues del proyecto](https://github.com/ctRl-ES/spanish_hip-hop/issues/) y, si puedes, ayuda en alguno.

## ¿Qué licencia tiene este proyecto?

[CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
