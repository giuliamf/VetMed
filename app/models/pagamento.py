from app import db

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consultas.id_consulta'), nullable=False)
    valor = db.Column(db.Numeric(15, 2), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    id_meio_pagamento = db.Column(db.Integer, db.ForeignKey('meios_pagamentos.id_meio_pagamento'), nullable=False)

    # Relacionamentos
    consulta = db.relationship('Consulta', backref='pagamentos')
    meio_pagamento = db.relationship('MeioPagamento', backref='pagamentos')

    def __repr__(self):
        return f"<Pagamento {self.id_pagamento}>"