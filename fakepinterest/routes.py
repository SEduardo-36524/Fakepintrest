# Cria as rotas do site (links)

# Bibliotecas
import os.path
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormCriarConta, FormLogin, FormFoto
from fakepinterest.models import Usuario, Post
from werkzeug.utils import secure_filename
import os

# Rota da homepage do site
@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    # Procura um usuário no banco de dados
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        # Caso um usuário for encontrado e a senha estiver correta
        # if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data): para bd local
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
            # Realiza o login
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

# Rota para criar uma conta
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criar_conta = FormCriarConta()
    # Funciona apenas se o usuário apertar no botão enviar e o formulário estiver preenchido e vfor válido
    if form_criar_conta.validate_on_submit():
        # Criptografa a senha
        # senha = bcrypt.generate_password_hash(form_criar_conta.senha.data) senha bd local
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode("utf-8")
        # Cria um usuario
        usuario = Usuario(username=form_criar_conta.username.data, 
                          senha=senha, 
                          email=form_criar_conta.email.data)
        # Armazena o usuário no banco de dados
        database.session.add(usuario)
        database.session.commit()
        # Permite o login
        login_user(usuario, remember=True)
        # Redireciona para a pagína de perfil
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criar_conta)

# Rota do perfil do usuário
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required # Permitido acessar apenas quando logado
def perfil(id_usuario):
    # Descobre se o usuário atual está logado
    if int(id_usuario) == int(current_user.id):
        # Carrega o formulário de fotos
        form_foto = FormFoto()
        # Trata o envio do arquivo(foto) para o banco de dados
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            # Cria um nome sem caracteres especiais 
            nome_seguro = secure_filename(arquivo.filename)
            # Caminho = (caminho do projeto (pasta onde está este arquivo "routes") + contante de upload + nome do arquivo)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], 
                              nome_seguro)
            # Salva o arquivo na pasta fotos_posts
            arquivo.save(caminho)
            # Registra o arquivo no banco de dados
            foto = Post(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else: 
        # Descobre o usuário de acordo com o id (caso não esteja no próprio perfil)
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

# Rota do logout do usuário
@app.route("/logout")
@login_required
def logout():
    # desloga o usuário atual
    logout_user()
    # Redireciona para a home page
    return redirect(url_for("homepage"))

# Rota para o feed
@app.route("/feed")
@login_required
def feed():
    # Obtém todas as fotos de todos os usuários para postar no feed, da mais recente para a menos recente (entre colchetes [:quantidade desejada])
    fotos = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)