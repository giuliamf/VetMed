import random

def gerar_crmv():
    # Código de estado (01 a 27)
    estado = random.randint(1, 27)
    estado_str = f"{estado:02d}"  # Formato de 2 dígitos

    # Número aleatório de 7 dígitos
    numero = random.randint(0, 9999999)
    numero_str = f"{numero:07d}"  # Formato de 7 dígitos

    # CRMV completo
    crmv = f"{estado_str}{numero_str}"
    return crmv