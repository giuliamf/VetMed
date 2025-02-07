import psycopg2

banco_existe = True

# Função para executar comandos SQL
def execute_sql(connection, sql_script):
    cursor = connection.cursor()
    try:
        cursor.execute(sql_script)
        print("Comando SQL executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")
    finally:
        cursor.close()

# Conecta ao banco de dados padrão (postgres)
conn = psycopg2.connect(
    dbname="postgres",  # Conecta ao banco de dados padrão
    user="postgres",    # Substitua pelo seu usuário
    password="123456789",  # Substitua pela sua senha
    host="localhost",
    port="5432"
)
conn.autocommit = True  # Habilita autocommit para comandos DDL (CREATE DATABASE, etc.)

if not banco_existe:
    # Lê e executa o arquivo criar_banco.sql
    with open(r"C:\Users\SuperUser\Documents\BDProjeto2024-2\criar_banco.sql", "r", encoding="utf-8") as file:
        criar_banco_script = file.read()
    execute_sql(conn, criar_banco_script)

    # Fecha a conexão atual
    conn.close()

# Conecta ao novo banco de dados (med_vet_bd)
conn = psycopg2.connect(
    dbname="med_vet_bd",  # Conecta ao banco de dados recém-criado
    user="postgres",      # Substitua pelo seu usuário
    password="123456789", # Substitua pela sua senha
    host="localhost",
    port="5432"
)
conn.autocommit = True

# Lê e executa o arquivo configurar_banco.sql
with open(r"C:\Users\SuperUser\Documents\BDProjeto2024-2\configurar_banco.sql", "r", encoding="utf-8") as file:
    configurar_banco_script = file.read()
execute_sql(conn, configurar_banco_script)

# Fecha a conexão
conn.close()