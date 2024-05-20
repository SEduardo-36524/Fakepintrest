# Cria a estrutura do banco de dados

# Bibliotecas
from fakepinterest import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

# Classes e funções

# Encontra o usuário para realizar login
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# Tabela do banco de dados
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Post", backref="usuario", lazy=True)


# Tabela do banco de dados
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)
