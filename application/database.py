import psycopg2
import traceback
import os


def connect_database():
    """ Conectar ao banco de dados PostgreSQL """
    user, password = 'postgres', 'giulia'
    try:
        connection = psycopg2.connect(
            dbname="vetmed",
            user=user,
            host='localhost',
            password=password,
            port='5432',
        )
        connection.autocommit = True
        c = connection.cursor()
        c.execute("SHOW client_encoding")
        print(c.fetchone())
        print("Conectado ao banco de dados com sucesso!")
        return c, connection
    except psycopg2.Error as e:
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            print(f"Erro no arquivo: {frame.filename}, linha {frame.lineno}, função {frame.name}")
        print(f"Mensagem do PostgreSQL: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        for frame in tb:
            print(f"Erro no arquivo: {frame.filename}, linha: {frame.lineno}, função: {frame.name}")

        print(f"Erro inesperado: {str(e)}")


def disconnect_database():
    """ Fecha a conexão com o banco """
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Conexão com o banco de dados fechada com sucesso!")
    except Exception as e:
        print(f"Erro ao fechar conexão com o banco de dados: {e}")


def create_tables():
    """ Executa o SQL de criação de tabelas do arquivo create_tables.sql """
    try:
        with open('database/create_tables.sql', 'r', encoding='utf-8') as file:
            sql_scrypt = file.read()
            cursor.execute(sql_scrypt)
            conn.commit()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")


def execute_sql(query, params=None, fetch_one=False, fetch_all=False):
    if not verify_connection():
        connect_database()
    """
    Executa um comando SQL genérico.

    :param query: A string da consulta SQL a ser executada.
    :param params: Parâmetros para a consulta SQL (evita SQL Injection).
    :param fetch_one: Se True, retorna apenas um único resultado.
    :param fetch_all: Se True, retorna todos os resultados da consulta.
    :return: Retorna os dados buscados no banco ou None se for um comando sem retorno.
    """
    print('Executando o SQL:', query)
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

        print(result)

        return result
    except Exception as e:
        print(f"Erro ao executar SQL: {e}")
        return None


def verify_connection():
    """ Verifica se a conexão com o banco de dados está ativa """
    global cursor, conn
    if conn is None or conn.closed or cursor is None:
        return False
    return True


""" FUNÇÕES DE MÉTODOS """


# Inicializando as variáveis globais cursor e conn


def globalizar_cursor_e_conexao():
    cursor, conn = connect_database()
    globals()['cursor'] = cursor
    globals()['conn'] = conn
    print("Variáveis globais cursor e conn inicializadas com sucesso!")


# Função específica para buscar usuários no banco
def buscar_dados_usuario_por_email(email):
    """ Retorna os dados de um usuário pelo email """
    query = "SELECT id_usuario, email, senha FROM Usuario WHERE email = %s"
    try:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result  # Retorna apenas um resultado
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None


def buscar_usuario_por_id(usuario_id):
    """ Retorna os dados de um usuário pelo ID """
    query = "SELECT id_usuario, nome, email FROM Usuario WHERE id_usuario = %s"
    try:
        cursor.execute(query, (usuario_id,))
        result = cursor.fetchone()
        return result  # Retorna apenas um resultado
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None


# criar UM usuario para entrar no sistema
def criar_usuario():
    """ Cria um usuário padrão para o sistema caso ele não exista """
    query_check = "SELECT 1 FROM Usuario WHERE email = %s"
    query = "INSERT INTO Usuario (nome, email, senha, cargo) VALUES (%s, %s, %s, %s)"
    params = ('admin', 'admin@vetmed.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'adm')

    try:
        usuario_existe = execute_sql(query_check, (params[1],), fetch_one=True)
        with open('static/profile_pictures/padrao.jpg', 'rb') as file:
            foto = file.read()
    except Exception as e:
        print(f"Erro ao verificar usuário padrão ou ao procurar a foto: {e}")
        usuario_existe = None

    query_foto = "INSERT INTO Usuario_Foto (id_usuario, foto) VALUES (%s, %s)"
    params_foto = (1, psycopg2.Binary(foto))

    if not usuario_existe:
        execute_sql(query, params)
        print('Usuário padrão criado com sucesso!')
        execute_sql(query_foto, params_foto)
        print('Foto padrão inserida com sucesso!')
    else:
        print('Usuário padrão já existe!')


""" Popular as tabelas automáticas """

base_dir = os.path.dirname(os.path.abspath(__file__))


# especialidade
def popular_especialidades():
    sql_file_path = os.path.join(base_dir, 'database', 'popular_especialidade.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        execute_sql(sql_script)
        print("Especialidades populadas com sucesso!")


def inicializar_status_agendamento():
    sql_file_path = os.path.join(base_dir, 'database', 'popular_status_agendamento.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        execute_sql(sql_script)
        print("Status populados com sucesso!")


def popular_horarios():
    sql_file_path = os.path.join(base_dir, 'database', 'popular_horarios.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        execute_sql(sql_script)
        print("Horários populados com sucesso!")


""""
def inicializar_tipo_consulta():
    sql_file_path = os.path.join(base_dir, 'database', 'popular_tipo_consulta.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        execute_sql(sql_script)
        print("Tipos de consulta populados com sucesso!")
"""