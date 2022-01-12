# AD-1 Servicios web


## Enunciado

Se pide programar un servicio web. Este servicio web deberá escuchar en el puerto 12345 y expondrá dos *endpoints:*

- El primero recibe una cadena de caracteres, de longitud arbitraria, y la almacena en un fichero en disco.
- El segundo recibirá una única palabra (sin espacios). Se devolverá el **número total** de las cadenas del citado fichero que la contengan, sin tener en cuenta:
    - Mayúsculas (*CADENA == Cadena*).
    - Posibles acentos (*avión == Avion*).
    - Múltiples apariciones en la misma cadena cuentan como una única.

Como **requisito**, el fichero donde se guardan los datos se debe persistir en disco y leerlo al arrancar el proceso. Si no existe, se creará vacío.

## Instalación Flask


🚨 Para instalar Flask vamos a utilizar `pip3`. Así que simplemente deberemos de escribir en nuestra línea de comandos lo siguiente:
```
  pip3 install Flask
```


## Explicación código

```python
from flask import Flask, jsonify, render_template
from werkzeug.routing import BaseConverter
import unicodedata
```

Usaremos Flask para la creación de nuestro server. Importaremos `jsonify` para responder con formato **json** y `render_template` para devolver una pagina web en la dirección principal del servidor.

Necesitaremos importar `BaseConverter` para poder crear una expresión regular y así controlar que recibiremos en el path.

Y por ultimo importaremos `unicodedata` para poder crear la función que remueva los acentos. 

```python
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    unaccented = only_ascii.decode('utf-8')
    return unaccented
```

Esta pieza de código nos devolverá un `string` sin acentos, que lo usaremos para la búsqueda de palabras en la base de datos.

```python
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
```

Necesitamos implementar la clase `RegexConverter` para poder usar una expresión regular, con lo que restringiremos las palabras que nos de el usuario a un patrón que hemos creado. En nuestro caso le hemos dicho que sea una palabra, con las letras A hasta la Z ( minúscula o mayúscula), que pueden llevar tilde y sin espacios.  Dicho patrón se lo asignaremos a la ruta que vamos a usar con el verbo `GET` para la búsqueda de una palabra en la base de datos.

```python
@app.route('/<regex("[a-zA-Z\u00E0-\u00FC]{0,}"):palabra>/', methods=['GET'])
def search(palabra):
    palabra = remove_accents(palabra)
    dataBase = open("bbdd.txt", "r")
    counter = 0
    for line in dataBase:
        if palabra.lower() in remove_accents(line.lower()):
            counter += 1
    return jsonify({'palabras encontradas': counter})
```

Haremos un bucle que recorra línea a línea el archivo de base de datos y si encuentra la palabra deseada nos lo sumara al contador y seguirá en la siguiente línea. Una vez recorrido todo el archivo nos devolverá la cifra de veces que ha cumplido la condición.

```python
@app.route('/<frase>', methods=['POST'])
def add(frase):
    dataBase = open("bbdd.txt", "a")
    dataBase.write(frase + "\n")
    dataBase.close()
    return jsonify({'message': 'Archivo agregado'})
```

Usaremos el verbo `POST` para añadir datos a la base de datos. Con la función `open("nombreArchivo","File Handling")` Crearemos el archivo si es que no existe y si existe le abriremos y escribiremos en el, sin sobrescribir los datos que existan en el. Para eso tenemos que pasarle el parámetro `“a”`. Escribimos la frase más un salto de línea y cerramos el archivo.

```python
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
```

En la ruta principal asignamos una pagina HTML con un poco de información. Para el correcto uso, tendremos que crear un directorio con el nombre Templates y ubicar ahí el archivo HTML y Css.

## Tecnologías usadas

- Python
- Flask
- werkzeug.routing
- Postman
- Notion
