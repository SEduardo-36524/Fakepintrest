# Bibliotecas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Cria o aplicativo
app = Flask(__name__)
# Local do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Chave de segurança do aplicativo
app.config["SECRET_KEY"] = "258c8aa7f0d8dcad40048a070d26c8bdfca4b5a1398f73da67dcc72ee3876351"
# Caminho de upload das fotos
app.config["UPLOAD_FOLDER"] = "static/fotos_post"

# Cria o banco de dados
database = SQLAlchemy(app)
# Criptografa a senha do usuário
bcrypt = Bcrypt(app)
# Gerencia o login do usuario
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

# Importa o arquivo de rotas
from fakepinterest import routes
