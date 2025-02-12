from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.database import criar_usuario, create_tables, globalizar_cursor_e_conexao, connect_database

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')     # Importa as configurações do arquivo config.py (createdb, createtables,
    # etc)
    app.secret_key = 'supersecretkey'
    
    db.init_app(app)

    with app.app_context():
        globalizar_cursor_e_conexao()
        create_tables()
        criar_usuario()

    # Registrar blueprints (rotas)

    from app.routes.tutor import tutores_bp
    app.register_blueprint(tutores_bp)

    from app.routes.animal import animais_bp
    app.register_blueprint(animais_bp)
    
    return app
