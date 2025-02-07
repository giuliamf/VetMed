from app import db


class Tutor(db.Model):
    __tablename__ = 'tutores'
    
    id_tutor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(15))
    endereço = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    
    animais = db.relationship('Animal', backref='tutor', lazy=True)
    
    def __repr__(self):
        return f"<Tutor {self.nome}>"