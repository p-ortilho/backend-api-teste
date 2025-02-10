from database.db_config import db

class Atendimentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Atendimento {self.id}>'