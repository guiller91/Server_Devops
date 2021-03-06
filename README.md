# AD-2 Unit Test

## Instalaci贸n Flask, Flask-Script y Coverage

馃毃 Para instalar Flask los m贸dulos necesarios vamos a utilizar `pip3`. As铆 que simplemente deberemos de escribir en nuestra l铆nea de comandos lo siguiente, uno por uno:

`pip3 install Flask==1.1.4`

`pip3 install Flask-Script`

`pip3 install coverage`


## Utilizaci贸n de manage.py

Si queremos iniciar el server : `python manage.py runserver`

Si queremos cambiar la direcci贸n y el puerto : `python manage.py runserver -h 0.0.0.0 -p 8080`

## Utilizaci贸n de la herramienta coverage

Para correr nuestros test: *`coverage run -m unittest discover tests/unit`*

Para generar un reporte de cobertura : `coverage report`

Si quieres ver la cobertura en un html : `coverage html`

## Explicaci贸n c贸digo

Usaremos Flask para la creaci贸n de nuestro server. Importaremos `jsonify` para responder con formato **json** y `render_template` para devolver una pagina web en la direcci贸n principal del servidor.

Necesitaremos importar `BaseConverter` para poder crear una expresi贸n regular y as铆 controlar que recibiremos en el path.

Y por ultimo importaremos `unicodedata` para poder crear la funci贸n que remueva los acentos. 

```python
from flask import Flask, jsonify, render_template
from werkzeug.routing import BaseConverter
import unicodedata
```

Esta pieza de c贸digo nos devolver谩 un `string` sin acentos, que lo usaremos para la b煤squeda de palabras en la base de datos:

```python
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    unaccented = only_ascii.decode('utf-8')
    return unaccented
```

Necesitamos implementar la clase `RegexConverter` para poder usar una expresi贸n regular, con lo que restringiremos las palabras que nos de el usuario a un patr贸n que hemos creado. En nuestro caso le hemos dicho que sea una palabra, con las letras A hasta la Z ( min煤scula o may煤scula), que pueden llevar tilde y sin espacios.  Dicho patr贸n se lo asignaremos a la ruta que vamos a usar con el verbo `GET` para la b煤squeda de una palabra en la base de datos.

```python
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
```

Haremos un bucle que recorra l铆nea a l铆nea el archivo de base de datos y si encuentra la palabra deseada nos lo sumara al contador y seguir谩 en la siguiente l铆nea. Una vez recorrido todo el archivo nos devolver谩 la cifra de veces que ha cumplido la condici贸n.

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

Usaremos el verbo `POST` para a帽adir datos a la base de datos. Con la funci贸n `open("nombreArchivo","File Handling")` Crearemos el archivo si es que no existe y si existe le abriremos y escribiremos en el, sin sobrescribir los datos que existan en el. Para eso tenemos que pasarle el par谩metro `鈥渁鈥漙. Escribimos la frase m谩s un salto de l铆nea y cerramos el archivo.

```python
@app.route('/<frase>', methods=['POST'])
def add(frase):
    dataBase = open("bbdd.txt", "a")
    dataBase.write(frase + "\n")
    dataBase.close()
    return jsonify({'message': 'Archivo agregado'})
```

## Tecnolog铆as usadas

- Python
- Flask 1.1.4
- werkzeug.routing
- Notion