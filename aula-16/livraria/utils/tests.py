from django.test import TestCase
from utils.utils import _retorna_digitos, valida_cpf


class TestPedido(TestCase):
    def setUp(self):
        pass

    def test_retorna_digitos(self):
        cpf = '123.456.789-10'
        digitos_cpf = _retorna_digitos(cpf)
        self.assertEqual(digitos_cpf, '12345678910')

    def test_retorna_cpf_valido(self):
        cpf_valido = '342.488.170-80'
        valido = valida_cpf(cpf_valido)
        self.assertTrue(valido)

    def test_retorna_cpf_invalido(self):
        cpf_invalido = '342.488.170-81'  # último dígito deveria ser 0
        valido = valida_cpf(cpf_invalido)
        self.assertFalse(valido)
