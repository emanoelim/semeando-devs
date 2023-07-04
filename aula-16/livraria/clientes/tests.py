from django.core.exceptions import ValidationError
from django.test import TestCase

from clientes.models import validator_cpf


class TestValidatorsCliente(TestCase):
    def setUp(self):
        pass

    def test_valida_cpf_valido(self):
        cpf_sem_mascara = '34248817080'
        cpf_mascarado = validator_cpf(cpf_sem_mascara)
        self.assertEqual(cpf_mascarado, '342.488.170-80')

    def test_valida_cpf_invalido(self):
        cpf_sem_mascara = '34248817081'  # último dígito deveria ser 0
        with self.assertRaises(ValueError):
            validator_cpf(cpf_sem_mascara)

