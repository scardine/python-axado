import requests


class Axado(object):
    def __init__(self, api_key, base_url='https://api.axado.com.br/v2/'):
        self.key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': self.key,
        }

    @staticmethod
    def json_wrapper(response):
        try:
            return response.json()
        except Exception as e:
            return {"error": u"{}".format(e)}

    def requests_wrapper(self, method, *args, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update(self.headers)
        kwargs.update({'headers': headers})
        try:
            r = getattr(requests, method)(*args, **kwargs)
        except Exception as e:
            return {"error": u"{}".format(e)}
        if r.status_code == 200:
            return self.json_wrapper(r)
        return {
            "error": "API error",
            "status_code": r.status_code,
            "data": self.json_wrapper(r)
        }

    def get(self, *args, **kwargs):
        return self.requests_wrapper('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requests_wrapper('post' *args, **kwargs)

    def consulta(self, cep_origem, cep_destino, volumes, valor_notafiscal, prazo_adicional=0,
                 preco_adicional=0,  fretegratis=False):
        return self.post(
            self.base_url + 'consulta',
            params={'token': self.key},
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


