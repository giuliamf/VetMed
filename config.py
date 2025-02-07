import psycopg2
from app import connect_database, disconnect_database, create_database

banco_existe = True


# Função para executar comandos SQL
def execute_sql(cursor, sql_script):
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
    password="giulia",  # Substitua pela sua senha
    host="localhost",
    port="5432"
)
conn.autocommit = True

create_database(conn.cursor(), 'VetMed')     # Criando o bd VetMed

# Conecta ao banco de dados padrão (postgres)
# Conecta ao novo banco de dados VetMed
cursor, conn = connect_database()   # Conecta ao banco de dados recém-criado

# Lê e executa o arquivo configurar_banco.sql
with open("configurar_banco.sql", "r", encoding="utf-8", errors="replace") as file:
    configurar_banco_script = file.read()


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:giulia@localhost:5432/VetMed'  # Modifique com suas credenciais
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evita avisos desnecessários


disconnect_database(cursor, conn)
