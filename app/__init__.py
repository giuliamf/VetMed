from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database import create_database

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'supersecretkey'
    
    db.init_app(app)
    create_database()   # para o banco de dados ser criado na inicialização do app, caso ele nao exista
    
    # Registrar blueprints (rotas)
    #from app.routes.animal_route import animais_bp
    from app.routes.tutores import tutores_bp
    #app.register_blueprint(animais_bp, url_prefix='/api')
    app.register_blueprint(tutores_bp, url_prefix='/api')
    
    return app