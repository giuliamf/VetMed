from app import db


class ReceitaMedica(db.Model):
    __tablename__ = 'receitas_medicas'

    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    id_tratamento = db.Column(db.Integer, db.ForeignKey('tratamentos.id_tratamento'), nullable=False)
    id_veterinario = db.Column(db.String(11), db.ForeignKey('veterinarios.id_veterinario'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    observacoes = db.Column(db.String(150))

    # Relacionamentos
    consulta = db.relationship('Consulta', backref='receitas_medicas')
    tratamento = db.relationship('Tratamento', backref='receitas_medicas')
    veterinario = db.relationship('Veterinario', backref='receitas_medicas')

    def __repr__(self):
        return f"<ReceitaMedica {self.id_receita}>"