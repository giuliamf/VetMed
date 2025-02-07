from app import db


class Tratamento(db.Model):
    __tablename__ = 'tratamentos'

    id_tratamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    tipo_tratamento = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    duracao_estimada = db.Column(db.String(50), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)

    # Relacionamento com a tabela Consultas
    consulta = db.relationship('Consulta', backref='tratamentos')

    def __repr__(self):
        return f"<Tratamento {self.id_tratamento}>"