from app.init import db


class TipoExame(db.Model):
    __tablename__ = 'tipos_exames'

    id_tipo_exame = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f"<TipoExame {self.nome}>"