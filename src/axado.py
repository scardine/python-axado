import requests

class STATUS_PEDIDO(object):
    AGUARDANDO_PAGAMENTO = 'pedido_esperando_pagamento'
    FATURADO = 'pedido_faturado'
    ENVIADO = 'pedido_enviado'
    ENTREGUE = 'pedido_entregue'
    CANCELADO = 'pedido_cancelado'


class Axado(object):
    def __init__(self, api_key, base_url='https://api.axado.com.br/v2/'):
        self._key = api_key
        self._base_url = base_url
        self._headers = {
            'Authorization': self._key,
        }
        self._params = {'token': self._key}

    @staticmethod
    def _json_wrapper(response):
        try:
            return response.json()
        except Exception as e:
            return {"error": u"{}".format(e)}

    @staticmethod
    def _digits_only(value):
        return "".join([_ for _ in value if _.isdigit()])

    def _requests_wrapper(self, method, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update(self._headers)
        kwargs.update({'headers': headers})
        try:
            r = getattr(requests, method)(*args, **kwargs)
        except Exception as e:
            return {"error": u"{}".format(e)}
        if 200 <= r.status_code <= 300:
            return self._json_wrapper(r)
        return {
            "error": "API error",
            "status_code": r.status_code,
            "data": self._json_wrapper(r)
        }

    def get(self, *args, **kwargs):
        return self._requests_wrapper('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._requests_wrapper('post', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._requests_wrapper('patch', *args, **kwargs)

    def cotacao(self, cep_origem, cep_destino, volumes, valor_notafiscal, prazo_adicional=0,
                preco_adicional=0, fretegratis=False):
        if '-' in cep_origem:
            cep_origem = self._digits_only(cep_origem)
        if '-' in cep_destino:
            cep_destino = self._digits_only(cep_destino)

        return self.post(
            self._base_url + 'consulta',
            params={'token': self._key},
            json={
                "cep_origem": cep_origem,
                "cep_destino": cep_destino,
                "valor_notafiscal": valor_notafiscal,
                "prazo_adicional": prazo_adicional,
                "preco_adicional": preco_adicional,
                "volumes": volumes,
                "fretegratis": fretegratis,
            }
        )

    def cotacao_consultar(self, token):
        return self.get(self._base_url + 'consulta/' + token, params=self._params)

    def pedido(self, consulta_token, cotacao_codigo, numero, status):
        params={'token': self._key}
        return self.post(
            self._base_url + 'pedido/',
            params=self._params,
            json={
                "consulta_token": consulta_token,
                "cotacao_codigo": cotacao_codigo,
                "numero": numero,
                "status": status,
            },
        )

    def pedido_consultar(self, pedido):
        return self.get(self._base_url + 'pedido/' + pedido, params=self._params)

    def pedido_atualizar(self, pedido, status):
        return self.patch(
            self._base_url + 'pedido/' + pedido,
            params=self._params,
            json={
                "status": status,
            }
        )

    def pedido_adicionar_nf(self, pedido, chave_acesso, cnpj_emitente, data_emissao, numero, serie,
                            valor_icms, valor_total, valor_frete):
        return self.patch(
            self._base_url + 'pedido/{}/notafiscal'.format(pedido),
            params=self._params,
            json={
                "chave_acesso": chave_acesso,
                "cnpj_emitente": cnpj_emitente,
                "data_emissao": data_emissao,
                "numero": numero,
                "serie": serie,
                "valor_icms": valor_icms,
                "valor_total": valor_total,
                "valor_frete": valor_frete,
            },
        )
