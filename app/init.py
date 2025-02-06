from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    # Registrar blueprints (rotas)
    from app.routes.animal_route import animais_bp
    from app.routes.tutores import tutores_bp
    app.register_blueprint(animais_bp, url_prefix='/api')
    app.register_blueprint(tutores_bp, url_prefix='/api')
    
    return app


def create_database(cursor, db_name='VetMed'):
    try:
        cursor.execute(f"""SELECT 1 FROM pg_database WHERE datname = {db_name};""")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"""
                CREATE DATABASE {db_name}
                WITH ENCODING 'UTF8'
                LC_COLLATE = 'pt_BR.UTF-8'
                LC_CTYPE = 'pt_BR.UTF-8'
                TEMPLATE template0;
""")
    except Exception as e:
        print(f'Erro: {e}')


def connect_database():
    user, password = 'postgres', 'giulia'
    conn = psycopg2.connect(dbname='VetMed', user=user, host='localhost', password=password, port='5432')
    conn.autocommit = True
    cursor = conn.cursor()

    return cursor, conn


def disconnect_database(cursor, conn):
    cursor.close()
    conn.close()
