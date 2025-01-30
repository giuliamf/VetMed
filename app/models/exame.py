from app import db

class Exame(db.Model):
    __tablename__ = 'exames'

    id_exame = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    id_animal = db.Column(db.Integer, db.ForeignKey('animais.id_animal'), nullable=False)
    id_tipo_exame = db.Column(db.Integer, db.ForeignKey('tipos_exames.id_tipo_exame'), nullable=False)
    resultado = db.Column(db.Text)
    data_exame = db.Column(db.Date, nullable=False)
    observacoes = db.Column(db.String(150))

    # Relacionamentos
    consulta = db.relationship('Consulta', backref='exames')
    animal = db.relationship('Animal', backref='exames')
    tipo_exame = db.relationship('TipoExame', backref='exames')

    def __repr__(self):
        return f"<Exame {self.id_exame}>"