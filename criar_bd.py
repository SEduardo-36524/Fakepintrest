# Biblioteca
from fakepinterest import database, app
from fakepinterest.models import Usuario, Post

# cria o banco de dados
with app.app_context():
    database.create_all()