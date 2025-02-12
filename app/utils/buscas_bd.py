from app.database import execute_sql


def buscar_cpf_tutor_por_id(id_tutor):
    query = "SELECT cpf FROM Tutor WHERE id_tutor = %s"
    cpf = execute_sql(query, (id_tutor,), fetch_one=True)
    return cpf[0] if cpf else None


def buscar_id_tutor_por_cpf(cpf):
    query = "SELECT id_tutor FROM Tutor WHERE cpf = %s"
    id_tutor = execute_sql(query, (cpf,), fetch_one=True)
    return id_tutor[0] if id_tutor else None


def buscar_id_tutor_por_id_animal(id_animal):
    query = "SELECT id_tutor FROM Animal WHERE id_animal = %s"
    id_tutor = execute_sql(query, (id_animal,), fetch_one=True)
    return id_tutor[0] if id_tutor else None


def buscar_animais_por_id_tutor(id_tutor):
    query = "SELECT * FROM Animal WHERE id_tutor = %s"
    animais = execute_sql(query, (id_tutor,), fetch_all=True)
    return animais if animais else None
