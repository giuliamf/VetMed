from app import db


class MeioPagamento(db.Model):
    __tablename__ = 'meios_pagamentos'

    id_meio_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<MeioPagamento {self.nome}>"