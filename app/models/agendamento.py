from app import db

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id_agendamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tutor = db.Column(db.Integer, db.ForeignKey('tutores.id_tutor'), nullable=False)
    id_animal = db.Column(db.Integer, db.ForeignKey('animais.id_animal'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'), nullable=False)

    # Relacionamentos
    tutor = db.relationship('Tutor', backref='agendamentos')
    animal = db.relationship('Animal', backref='agendamentos')
    status = db.relationship('Status', backref='agendamentos')

    def __repr__(self):
        return f"<Agendamento {self.id_agendamento}>"