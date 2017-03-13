import random
import unittest
from axado import Axado, STATUS_PEDIDO
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
        result = self.api.cotacao(
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
        return result

    def test_consulta_cep_with_dash(self):
        result = self.api.cotacao(
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
        self.assertIn('error', self.api.cotacao('', '', [], ''))

    def test_consultar_cotacao(self):
        result = self.test_consulta()
        token = result['consulta_token']
        self.assertIn('consulta_token', self.api.cotacao_consultar(token))

    def test_pedido(self):
        result = self.test_consulta()
        token = result['consulta_token']
        result = self.api.pedido(
            consulta_token=token,
            cotacao_codigo="1",
            numero=str(random.randint(1, 100000)),
            status=STATUS_PEDIDO.AGUARDANDO_PAGAMENTO,
        )
        self.assertIn('numero', result)
        self.assertIn('consultas', result)
        self.assertIn('status', result)
        self.assertIn('data_cadastro', result)
        return result

    def test_consultar_pedido(self):
        result = self.test_pedido()
        pedido = result['numero']
        result = self.api.pedido_consultar(pedido)

    def test_atualizar_pedido(self):
        result = self.test_pedido()
        pedido = result['numero']
        result = self.api.pedido_atualizar(pedido, STATUS_PEDIDO.CANCELADO)

    def test_adicionar_nota_fiscal_ao_pedido(self):
        result = self.test_pedido()
        pedido = result['numero']
        result = self.api.pedido_adicionar_nf(
            pedido=pedido,
            chave_acesso='01234567890123456789012345678901234567891234',
            cnpj_emitente='12345678901234',
            data_emissao='2015-01-13T23:01:22Z',
            numero='12345',
            serie='3',
            valor_icms='0',
            valor_total='71.89',
            valor_frete='1.99',
        )
        self.assertIn('chave_acesso', result)
        self.assertIn('numero', result)
        self.assertIn('serie', result)
        return result


if __name__ == '__main__':
    unittest.main()