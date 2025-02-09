import hashlib


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_senha(senha, senha_hash):
    return criptografar_senha(senha) == senha_hash

"""
print(criptografar_senha('giulia'), verificar_senha('GiuLIA', 'e4c2eed8a6df0147265631e9ff25b70fd0e4b3a246896695b089584bf3ce8b90'))
print(criptografar_senha('celio'), verificar_senha('celio', '60fe67ed8156498b9a17f3d983bcf3961d7aa8c36e33bf2edf2ccf1706d33fef'))
print(criptografar_senha('analuiza'), verificar_senha('analuiza', '0a3fa8009c0f56804c7bee62f18836d7bf84743d7ba2b2d0fb151e03b71a6b81'))
"""