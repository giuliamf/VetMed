from app import db

class ReceitaMedicamento(db.Model):
    __tablename__ = 'receita_medicamento'

    id_receita = db.Column(db.Integer, db.ForeignKey('receitas_medicas.id_receita'), primary_key=True)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamentos.id_medicamento'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo_quantidade = db.Column(db.String(5), nullable=False)
    frequencia = db.Column(db.String(25), nullable=False)
    duracao = db.Column(db.String(75), nullable=False)

    # Relacionamentos
    receita = db.relationship('ReceitaMedica', backref='receita_medicamentos')
    medicamento = db.relationship('Medicamento', backref='receita_medicamentos')

    def __repr__(self):
        return f"<ReceitaMedicamento Receita: {self.id_receita}, Medicamento: {self.id_medicamento}>"