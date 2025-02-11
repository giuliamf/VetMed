import psycopg2


def connect_database():
    """ Conectar ao banco de dados PostgreSQL """
    user, password = 'postgres', 'giulia'
    conn = psycopg2.connect(
        dbname='VetMed',
        user=user,
        host='localhost',
        password=password,
        port='5432',
        client_encoding="utf8"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return cursor, conn


def disconnect_database(cursor, conn):
    """ Fecha a conexão com o banco """
    cursor.close()
    conn.close()


def create_database(cursor, db_name):
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


def create_tables(cursor):
    """ Cria as tabelas a partir do arquivo SQL """
    try:
        with open('app/database/create_tables.sql', 'r') as file:
            cursor.execute(file.read())
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


def execute_sql(cursor, sql_script):
    """ Executa um comando SQL genérico """
    try:
        cursor.execute(sql_script)
        print("Comando SQL executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")
