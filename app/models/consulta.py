from app import db

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id_consulta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_animal = db.Column(db.Integer, db.ForeignKey('animais.id_animal'), nullable=False)
    id_veterinario = db.Column(db.String(11), db.ForeignKey('veterinarios.id_veterinario'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos.id_tipo'), nullable=False)

    # Relacionamentos
    animal = db.relationship('Animal', backref='consultas')
    veterinario = db.relationship('Veterinario', backref='consultas')
    tipo = db.relationship('Tipo', backref='consultas')

    def __repr__(self):
        return f"<Consulta {self.id_consulta}>"