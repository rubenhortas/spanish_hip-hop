# tools

## ¿Qué son estas herramientas?

Estas herramientas son pequeños scripts en python para mantener el fichero [lista trabajos hip-hop español.csv](https://github.com/ctRl-ES/spanish_hip-hop/edit/master/lista%20trabajos%20hip-hop%20espa%C3%B1ol.csv).

## ¿Para qué valen estas herramientas?

## check_exceptions.py
Genera tres ficheros:
  * `lines_with_exceptions.txt`: Líneas **con** excepciones en los artistas/títulos.
  * `lines_without_exceptions.txt`: Líneas **sin** excepciones en los artistas/títulos.
  * `unused_exceptions.txt`: Excepciones que no se utilizan.  
    Es útil para ver las transformaciones que se producen al formatear el fichero y para manter reducido el número de excepciones que contiene el diccionario `exceptions.py`.

## generate_exceptions_dictionary.py
Genera un nuevo diccionario de excepciones (exceptions.py), a partir del actual, ordenado alfabéticamente y sin duplicados.  
Es útil para desarrollo.

### format_file.py

Formatea las líneas del fichero [lista trabajos hip-hop español.csv](https://github.com/ctRl-ES/spanish_hip-hop/edit/master/lista%20trabajos%20hip-hop%20espa%C3%B1ol.csv) para que todas las líneas tengan un formato homogéneo.  
Este script generará un fichero llamado `lista trabajos hip-hop español - formateado.csv`.

### generate_exceptions_dictionary.py

Genera el diccionario de excepciones (`exceptions.py`) ordenado alfabéticamente y sin duplicados.  
Es útil para desarrollo.

### get_duplicates.py

Genera el fichero `duplicados.txt` con las entradas [posiblemente] repetidas en el fichero [lista trabajos hip-hop español.csv](https://github.com/ctRl-ES/spanish_hip-hop/edit/master/lista%20trabajos%20hip-hop%20espa%C3%B1ol.csv) para poder eliminarlas rápidamente.

## ¿Cómo se utilizan estas herramientas?

Coloca el el fichero `lista trabajos hip-hop español.csv` en el directorio de  los scripts y ejecuta el script escogido.

## ¿Cómo colaborar?

* Date de alta en github

    * Sube nuevos scripts que aporten nuevas funcionalidades.
    * Corrige errores (o añade nuevas funcionalidades) en los scripts de herramientas.
    * Aporta nuevas herramientas que ayuden a la gestión de este proyecto.

* Echa un ojo a los [Issues del proyecto](https://github.com/ctRl-ES/spanish_hip-hop/issues/) y ayuda en alguno.

## ¿Qué licencia tiene este proyecto?

[CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
