from django.db import models
from django.core.exceptions import ValidationError

from services.cep_service import CepService
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
    

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)

    def preencher_endereco(self):
        service = CepService()
        try:
            endereco = service.consultar_cep(self.cep)
            self.rua = endereco.get('logradouro')
            self.cidade = endereco.get('localidade')
            self.uf = endereco.get('uf')
            self.save()
        except Exception:
            pass


    def __str__(self) -> str:
        return f'{self.cliente.nome}'
