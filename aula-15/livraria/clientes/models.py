from django.db import models
from django.core.exceptions import ValidationError

from utils.utils import valida_cpf, mascara_cpf


def validator_cpf(value):
    if not valida_cpf(value):
        raise ValidationError('CPF inválido.')
    return mascara_cpf(value)


class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, validators=[validator_cpf])  # com a máscara
    data_nascimento = models.DateField()
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nome} - {self.cpf}'

