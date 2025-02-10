from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
import os
from flask_cors import CORS

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.config['SECRET_KEY'] = secrets.token_hex(64)

    # Criar o caminho absoluto para o banco de dados
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    return app
