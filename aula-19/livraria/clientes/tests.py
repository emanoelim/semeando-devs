from model_bakery import baker
from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory

from clientes.models import Cliente, Endereco, validator_cpf
from clientes.views import EnderecoView
from services.cep_service import CepService


mock_cep_service = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "complemento": "lado ímpar",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
        "ibge": "3550308",
        "gia": "1004",
        "ddd": "11",
        "siafi": "7107"
}


class TestValidatorsCliente(TestCase):
    def setUp(self):
        pass

    def test_valida_cpf_valido(self):
        cpf_sem_mascara = '34248817080'
        cpf_mascarado = validator_cpf(cpf_sem_mascara)
        self.assertEqual(cpf_mascarado, '342.488.170-80')

    def test_valida_cpf_invalido(self):
        cpf_sem_mascara = '34248817081'  # último dígito deveria ser 0
        with self.assertRaises(ValidationError):
            validator_cpf(cpf_sem_mascara)


class TestEnderecoView(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.cliente = baker.make(Cliente)
        self.data = {
            'cliente': self.cliente.id,
            'cep': '01001000',
            'numero': 200
        }

    def _post_request(self, data):
        request = self.factory.post('/clientes/enderecos/', data, format='json')
        view = EnderecoView.as_view({'post': 'create'})
        return view(request)
    
    def _put_request(self, data, pk):
        request = self.factory.put(f'/clientes/enderecos/', data, format='json')
        view = EnderecoView.as_view({'put': 'update'})
        return view(request, pk=pk)

    @patch.object(CepService, 'consultar_cep', Mock(return_value=mock_cep_service))
    def test_endereco_preenchido_create(self):
        resposta = self._post_request(self.data)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')

    @patch.object(CepService, 'consultar_cep', Mock(return_value=mock_cep_service))
    def test_endereco_preenchido_update(self):
        endereco = baker.make(Endereco)
        resposta = self._put_request(self.data, endereco.id)
        self.assertEqual(resposta.data['rua'], 'Praça da Sé')
        self.assertEqual(resposta.data['cidade'], 'São Paulo')
        self.assertEqual(resposta.data['uf'], 'SP')
