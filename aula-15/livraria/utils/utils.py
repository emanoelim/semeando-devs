def _retorna_digitos(texto):
    if not texto or not isinstance(texto, str):
        return None
    return ''.join([c for c in texto if c.isdigit()])

def valida_cpf(cpf):
    cpf = _retorna_digitos(cpf)
    if not cpf or len(cpf) != 11:
        return False

    # Primeiro dígito
    relacao_digito_peso = zip(
        [int(digito) for digito in cpf[0:-2]], [peso for peso in range(10, 1, -1)])
    resto_soma = sum(
        [digito * peso for digito, peso in relacao_digito_peso]) % 11
    digito_esperado = 11 - resto_soma if resto_soma >= 2 else 0
    if cpf[-2] != str(digito_esperado):
        return False

    # Segundo dígito
    relacao_digito_peso = zip(
        [int(digito) for digito in cpf[0:-1]], [peso for peso in range(11, 1, -1)])
    resto_soma = sum(
        [digito * peso for digito, peso in relacao_digito_peso]) % 11
    digito_esperado = 11 - resto_soma if resto_soma >= 2 else 0
    if cpf[-1] != str(digito_esperado):
        return False

    return True


def mascara_cpf(cpf):
    if valida_cpf(cpf):
        cpf = _retorna_digitos(cpf)
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    return None
