from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    # Registrar blueprints (rotas)
    from app.routes.animais import animais_bp
    from app.routes.tutores import tutores_bp
    app.register_blueprint(animais_bp)
    app.register_blueprint(tutores_bp)
    
    return app
