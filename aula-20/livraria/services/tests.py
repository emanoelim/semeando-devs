from unittest import skip

from django.test import TestCase

from services.cep_service import CepService


class TestCepService(TestCase):
    def setUp(self) -> None:
        self.service = CepService()

    @skip('Acessa a API')
    def test_consultar_cep(self):
        reposta = self.service.consultar_cep('01001000')
        self.assertEqual(reposta.get('cep'), '01001-000')