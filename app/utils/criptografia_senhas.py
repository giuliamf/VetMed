import hashlib


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_senha(senha, senha_hash):
    return criptografar_senha(senha) == senha_hash
