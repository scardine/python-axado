import unittest
from axado import Axado
try:
    from settings import KEY
except ImportError:
    print('''Please, create a settings.py file containing "KEY='XXXXXX'"
    where 'XXXXXX' is your API key obtained at http://www.axado.com.br''')

class TestConsulta(unittest.TestCase):
    def setUp(self):
        self.api = Axado(KEY)

    def test_digits(self):
        self.assertNotIn('-', self.api._digits_only('12345-678'))

    def test_consulta(self):
        result = self.api.consulta(
            '04544051',
            '04568000',
            [
                {
                    "sku": "A-01",
                    "quantidade": "1",
                    "preco": "15,20",
                    "altura": "35",
                    "comprimento": "10",
                    "largura": "30",
                    "peso": "2",
                }
            ],
            "15,20",
        )
        self.assertIn('consulta_token', result)

    def test_consulta_cep_with_dash(self):
        result = self.api.consulta(
            '04544-051',
            '04568-000',
            [
                {
                    "sku": "A-01",
                    "quantidade": "1",
                    "preco": "15,20",
                    "altura": "35",
                    "comprimento": "10",
                    "largura": "30",
                    "peso": "2",
                }
            ],
            "15,20",
        )
        self.assertIn('consulta_token', result)

    def test_error_wrapping(self):
        self.assertIn('error', self.api.consulta('', '', [], ''))

    def test_consulta_token(self):
        result = self.api.consulta(
            '04544051',
            '04568000',
            [
                {
                    "sku": "A-01",
                    "quantidade": "1",
                    "preco": "15,20",
                    "altura": "35",
                    "comprimento": "10",
                    "largura": "30",
                    "peso": "2",
                }
            ],
            "15,20",
        )
        token = result['consulta_token']
        self.assertIn('consulta_token', self.api.consulta_token(token))

    def test_pedido(self):
        result = self.api.pedido(
            consulta_token="a326d58ba2833313ac6ca716a5e6041a",
            cotacao_codigo="2",
            numero="1234",
            status="pedido_esperando_pagamento"
        )
        self.assertIn('pedido', result)


if __name__ == '__main__':
    unittest.main()