# AD-2 Unit Test

## Miembros del grupo:

- [Iván Gaitán Muñoz](https://github.com/IGaitanM)
- [Luz Maria Lozano Asimbaya](https://github.com/luzlozas)
- [Miguel Pérez Larren](https://github.com/miguelperezlarren)
- [Guillermo Pérez Arias](https://github.com/guiller91)
- [Sarah Amselem Felices](https://github.com/saramselem)

## Repositorio:

[GitHub - guiller91/Server_Devops: Un servidor que almacena String y consulta palabras.](https://github.com/guiller91/Server_Devops)

## 

## Instalación Flask, Flask-Script y Coverage


🚨 Para instalar Flask los módulos necesarios vamos a utilizar `pip3`. Así que simplemente deberemos de escribir en nuestra línea de comandos lo siguiente, uno por uno:

`pip3 install Flask==1.1.4`

`pip3 install Flask-Script`

`pip3 install coverage`



## Utilización de manage.py

Si queremos iniciar el server : `python manage.py runserver`

Si queremos cambiar la dirección y el puerto : `python manage.py runserver -h 0.0.0.0 -p 8080`

## Utilización de la herramienta coverage

Para correr nuestros test: *`coverage run -m unittest discover tests/unit`*

Para generar un reporte de cobertura : `coverage report`

Si quieres ver la cobertura en un html : `coverage html`

## Explicación código

Usaremos Flask para la creación de nuestro server. Importaremos `jsonify` para responder con formato **json** y `render_template` para devolver una pagina web en la dirección principal del servidor.

Necesitaremos importar `BaseConverter` para poder crear una expresión regular y así controlar que recibiremos en el path.

Y por ultimo importaremos `unicodedata` para poder crear la función que remueva los acentos. 

```python
from flask import Flask, jsonify, render_template
from werkzeug.routing import BaseConverter
import unicodedata
```

Esta pieza de código nos devolverá un `string` sin acentos, que lo usaremos para la búsqueda de palabras en la base de datos:

```python
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    unaccented = only_ascii.decode('utf-8')
    return unaccented
```

Necesitamos implementar la clase `RegexConverter` para poder usar una expresión regular, con lo que restringiremos las palabras que nos de el usuario a un patrón que hemos creado. En nuestro caso le hemos dicho que sea una palabra, con las letras A hasta la Z ( minúscula o mayúscula), que pueden llevar tilde y sin espacios.  Dicho patrón se lo asignaremos a la ruta que vamos a usar con el verbo `GET` para la búsqueda de una palabra en la base de datos.

```python
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
```

Haremos un bucle que recorra línea a línea el archivo de base de datos y si encuentra la palabra deseada nos lo sumara al contador y seguirá en la siguiente línea. Una vez recorrido todo el archivo nos devolverá la cifra de veces que ha cumplido la condición.

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

Usaremos el verbo `POST` para añadir datos a la base de datos. Con la función `open("nombreArchivo","File Handling")` Crearemos el archivo si es que no existe y si existe le abriremos y escribiremos en el, sin sobrescribir los datos que existan en el. Para eso tenemos que pasarle el parámetro `“a”`. Escribimos la frase más un salto de línea y cerramos el archivo.

```python
@app.route('/<frase>', methods=['POST'])
def add(frase):
    dataBase = open("bbdd.txt", "a")
    dataBase.write(frase + "\n")
    dataBase.close()
    return jsonify({'message': 'Archivo agregado'})
```

## Tecnologías usadas

- Python
- Flask 1.1.4
- werkzeug.routing
- Notion