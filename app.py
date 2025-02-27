from datetime import timedelta
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from modelo.Rango import Rango
from modelo.ListaUsers import ListaUsers
from modelo.User import Usuario


app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app)
listaUsers = ListaUsers()

@login_manager.user_loader
def load_user(user_id : int):
    for user in listaUsers.users:
        if user.id == user_id:
            return user
    return None

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")
        usuAux = listaUsers.get_user(email)

        if usuAux is not None and usuAux.check_password(contraseña):
            login_user(usuAux, remember=True, duration=timedelta(hours=1))
            print("Usuario {} logueado".format(current_user.nombre))
            return redirect(url_for("index"))
    
    return render_template('login_form.html')

@app.route("/logon", methods=["GET", "POST"])
def logon():
    # Solo puede acceder el senséi
    if current_user.rango != Rango.SENSEI:
        print("Acceso no autorizado")
        return redirect(url_for("index"))
    
    return render_template("logon_form.html")

@app.route('/logout')
def logout():
    print("Se va a cerrar sesión de usuario")
    logout_user()
    return redirect(url_for('index'))