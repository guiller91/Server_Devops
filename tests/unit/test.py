from aplicacion.server import app, remove_accents
import unittest


# Comando para correr todos los tests:
# coverage run -m unittest discover tests/unit

class TestFlaskApi(unittest.TestCase):

    def test_add(self):
        tester = app.test_client(self)
        response = tester.post('/hola')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_add_2(self):
        tester = app.test_client(self)
        response = tester.post('/hola')
        self.assertEqual(response.content_type, "application/json")

    def test_search(self):
        tester = app.test_client(self)
        response = tester.get('/hola')
        status_code = response.status_code
        self.assertEqual(status_code, 308 or 200)

    def test_search_2(self):
        tester = app.test_client(self)
        response = tester.get('/hola')
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_search_fail(self):
        tester = app.test_client(self)
        response = tester.get('/121')
        status_code = response.status_code
        self.assertEqual(status_code, 405)

    def test_search_fail_2(self):
        tester = app.test_client(self)
        response = tester.get('/hola que tal')
        status_code = response.status_code
        self.assertEqual(status_code, 405)

    def test_remove_accents(self):
        self.assertEqual(remove_accents("áéíóú"), "aeiou")
        self.assertEqual(remove_accents("ÁÉÍÓÚ"), "AEIOU")
        self.assertEqual(remove_accents("ÁÉÍÓÚÑ"), "AEIOUN")
        self.assertEqual(remove_accents("áéíóúñ"), "aeioun")
        self.assertEqual(remove_accents("áéíóúñÑ"), "aeiounN")


if __name__ == "__main__":
    unittest.main()
