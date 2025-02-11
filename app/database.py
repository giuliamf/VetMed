import psycopg2


def connect_database():
    """ Conectar ao banco de dados PostgreSQL """
    user, password = 'postgres', 'giulia'
    connection = psycopg2.connect(
        dbname='VetMed',
        user=user,
        host='localhost',
        password=password,
        port='5432',
        client_encoding="utf8"
    )
    conn.autocommit = True
    c = conn.cursor()
    return c, connection


def disconnect_database():
    """ Fecha a conexão com o banco """
    global cursor, conn
    cursor.close()
    conn.close()


def create_database():
    db_name = 'VetMed'

    """ Cria o banco de dados caso ele não exista """
    try:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE \"{db_name}\" "
                           f"ENCODING 'UTF8' "
                           f"LC_COLLATE 'pt_BR.UTF-8' "
                           f"LC_CTYPE 'pt_BR.UTF-8' "
                           f"TEMPLATE template0;")
            print(f'Banco de dados >{db_name}< criado com sucesso!')
        else:
            print(f'Banco de dados >{db_name}< já existe!')
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')


def create_tables():
    """ Executa o SQL de criação de tabelas do arquivo create_tables.sql """
    global cursor, conn
    try:
        with open('app/database/create_tables.sql', 'r', encoding='utf-8') as file:
            sql_scrypt = file.read()
            cursor.execute(sql_scrypt)
            conn.commit()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


def execute_sql(query, params=None, fetch_one=False, fetch_all=False):
    """
    Executa um comando SQL genérico.

    :param query: A string da consulta SQL a ser executada.
    :param params: Parâmetros para a consulta SQL (evita SQL Injection).
    :param fetch_one: Se True, retorna apenas um único resultado.
    :param fetch_all: Se True, retorna todos os resultados da consulta.
    :return: Retorna os dados buscados no banco ou None se for um comando sem retorno.
    """
    global cursor, conn
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch_one:
            result = cursor.fetchone()  # Retorna apenas um resultado
        elif fetch_all:
            result = cursor.fetchall()  # Retorna todos os resultados
        else:
            conn.commit()  # Confirma transações como INSERT, UPDATE, DELETE
            result = None

        return result
    except Exception as e:
        print(f"Erro ao executar SQL: {e}")
        return None


""" FUNÇÕES DE MÉTODOS """
# Criar conexão única no início
cursor, conn = connect_database()


# Função específica para buscar usuários no banco
def buscar_dados_usuario_por_email(email):
    """ Retorna os dados de um usuário pelo email """
    query = "SELECT id_usuario, email, senha FROM Usuario WHERE email = %s"
    return execute_sql(query, (email,), fetch_one=True)     # Retorna apenas um resultado


def buscar_usuario_por_id(usuario_id):
    """ Retorna os dados de um usuário pelo ID """
    query = "SELECT id_usuario, nome, email, cargo FROM Usuario WHERE id_usuario = %s"
    return execute_sql(query, (usuario_id,), fetch_one=True)
