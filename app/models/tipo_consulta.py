from app.init import db


class Tipo(db.Model):
    __tablename__ = 'tipos'

    id_tipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50))
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f"<Tipo {self.nome}>"