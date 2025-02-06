from app.init import db


class Animal(db.Model):
    __tablename__ = 'animais'

    id_animal = db.Column(db.Integer, primary_key=True)  # Gerado automaticamente pelo banco
    id_tutor = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    ano_nascimento = db.Column(db.Integer)
    sexo = db.Column(db.String(1), nullable=False)  # 'Macho' ou 'Fêmea'
    peso = db.Column(db.String(20))
    cor = db.Column(db.String(30))

    def __repr__(self):
        return f"<Animal {self.nome} ({self.id_animal})>"
