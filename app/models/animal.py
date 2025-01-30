from app import db

class Animal(db.Model):
    __tablename__ = 'animais'
    
    id_animal = db.Column(db.Integer, primary_key=True)
    id_tutor = db.Column(db.Integer, db.ForeignKey('tutores.id_tutor'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    ano_nascimento = db.Column(db.Integer)
    sexo = db.Column(db.String(1))
    peso = db.Column(db.Float)
    cor = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<Animal {self.nome}>"
