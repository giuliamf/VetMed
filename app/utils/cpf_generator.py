import random

def calcular_digito_verificador(cpf_base):
    """Calcula os dígitos verificadores de um CPF."""
    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_base[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Cálculo do segundo dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_base[i]) * (11 - i)
    soma += digito1 * 2
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return f"{digito1}{digito2}"

def gerar_cpf():
    """Gera um CPF válido no formato brasileiro."""
    # Gera os 9 primeiros dígitos aleatoriamente
    cpf_base = ''.join([str(random.randint(0, 9)) for _ in range(9)])

    # Calcula os dígitos verificadores
    digito_verificador = calcular_digito_verificador(cpf_base)

    # Retorna o CPF completo
    cpf = f"{cpf_base}{digito_verificador}"
    return cpf