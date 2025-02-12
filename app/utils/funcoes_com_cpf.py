from app.database import execute_sql
from flask import jsonify
import re


# Função para verificar se o cpf está cadastrado no banco de dados
def cpf_existe(cpf):
    query_verificar = "SELECT COUNT(*) FROM Tutor WHERE cpf = %s"
    resultado = execute_sql(query_verificar, (cpf,), fetch_one=True)

    if resultado and resultado[0] > 0:
        return jsonify({"erro": "CPF já cadastrado!"}), 400
    return None


# Função para verificar se o novo cpf é igual ao cpf atual
def cpf_igual(cpf, id_tutor):
    query_verificar = "SELECT cpf FROM Tutor WHERE id_tutor = %s"
    resultado = execute_sql(query_verificar, (id_tutor,), fetch_one=True)

    if resultado and cpf == resultado[0]:
        return True
    return False


# Função para formatar o cpf
def formatar_cpf(cpf):
    print(cpf)
    cpf = re.sub(r'\D', '', cpf)  # Remove tudo que não for número
    print(f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


# Função para achar o nome do tutor através do cpf
def nome_tutor_cpf(cpf):
    query = "SELECT nome FROM Tutor WHERE cpf = %s"
    nome = execute_sql(query, (cpf,), fetch_one=True)
    return nome[0] if nome else None


# Função para achar o nome do tutor através do id
def nome_tutor_id(id_tutor):
    query = "SELECT nome FROM Tutor WHERE id_tutor = %s"
    nome = execute_sql(query, (id_tutor,), fetch_one=True)
    return nome[0] if nome else None
