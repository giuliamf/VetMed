import os

class Config:
    # Configurações do banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@localhost:5432/seu_banco_de_dados')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
