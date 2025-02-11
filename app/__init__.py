from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'supersecretkey'
    
    db.init_app(app)
    
    # Registrar blueprints (rotas)
    #from app.routes.animal_route import animais_bp
    from app.routes.tutores import tutores_bp
    #app.register_blueprint(animais_bp, url_prefix='/api')
    app.register_blueprint(tutores_bp, url_prefix='/api')
    
    return app


def create_database(cursor, db_name):
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


def connect_database():
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
    cursor.close()
    conn.close()


def create_tables(cursor):
    # Aqui deve chamar um arquivo .sql com os comandos de criação das tabelas
    with open('app/database/create_tables.sql', 'r') as file:
        cursor.execute(file.read())


# Função para executar comandos SQL
def execute_sql(cursor, sql_script):
    try:
        cursor.execute(sql_script)
        print("Comando SQL executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar o script SQL: {e}")
