# Python Axado

Python bindings to the Axado API (https://developers.axado.com.br/)

At the moment this is not officially endorsed by Axado.

## Usage

Get an API instance using your API key and call API methods:

    axado = Achado('3243a88778b78788c878786d652ee')
    axado.consulta(
            cep_origem='04544051',
            cep_destino'04568000',
            volumes=[
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
            valor_notafiscal="15,20",    
    )