from database.db_config import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)


    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return f'<Usuario {self.email}>'
