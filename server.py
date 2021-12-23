from flask import Flask, jsonify
from werkzeug.routing import BaseConverter
import unicodedata
app = Flask(__name__)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    frase = only_ascii.decode('utf-8')
    return frase


# lo necesitaremos para poder usar una expresion regular en el path
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/<frase>', methods=['POST'])
def add(frase):
    dataBase = open("bbdd.txt", "a")
    dataBase.write(frase + "\n")
    dataBase.close()
    return jsonify({'message': 'Archivo agregado'})


@app.route('/<regex("[a-zA-Z\u00E0-\u00FC]{0,}"):palabra>/', methods=['GET'])
def search(palabra):
    palabra = remove_accents(palabra)
    dataBase = open("bbdd.txt", "r")
    contador = 0
    for line in dataBase:
        if palabra.lower() in remove_accents(line.lower()):
            contador += 1
    return jsonify({'palabras encontradas': contador})


if __name__ == '__main__':
    app.run(debug=True, port=12345)
