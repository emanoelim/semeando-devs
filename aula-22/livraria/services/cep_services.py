import json
import requests


class CepService:
    def __init__(self):
        self.url = 'https://viacep.com.br/ws'

    def consultar_cep(self, cep):
        # montar url no formato esperado (https://viacep.com.br/ws/85501352/json/)
        url = f'{self.url}/{cep}/json/'
        resposta = requests.get(url)
        resposta_text = resposta.text
        resposta_json = json.loads(resposta_text)
        return resposta_json
