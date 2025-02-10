from database.db_config import db

class Servicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco
        }

    def __repr__(self):
        return f'<Servico {self.nome}>'

