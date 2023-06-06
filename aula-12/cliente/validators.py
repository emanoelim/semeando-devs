from utils.utils import valida_cpf, mascara_cpf


def cpf_valido(value, name):
    if not valida_cpf(value):
        raise ValueError('CPF inválido.')
    return mascara_cpf(value)
