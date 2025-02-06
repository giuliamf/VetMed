from app.init import db


class Status(db.Model):
    __tablename__ = 'status'

    id_status = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Status {self.nome}>"