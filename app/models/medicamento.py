from app import db

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'

    id_medicamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(70), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    uso = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"<Medicamento {self.nome}>"