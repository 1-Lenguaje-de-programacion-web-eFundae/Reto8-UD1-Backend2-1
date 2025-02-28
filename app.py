from datetime import date, datetime, timedelta
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from modelo.Salas import Salas
from modelo.ListaReserva import ListaReservas
from modelo.Rango import Rango
from modelo.ListaUsers import ListaUsers
from modelo.User import Usuario
from modelo.Reserva import Reserva


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
    # Si ya ha iniciado sesión
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
    if current_user.is_anonymous or current_user.rango != Rango.SENSEI:
        print("Acceso no autorizado")
        return redirect(url_for("index"))
    
    return render_template("logon_form.html")

@app.route('/logout')
def logout():
    print("Se va a cerrar sesión de usuario")
    logout_user()
    return redirect(url_for('index'))

@app.route("/nueva-reserva")
def reserva():
    # Se debe iniciar sesión para reservar sala
    if current_user.is_anonymous:
        print("Acceso no autorizado")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        salaStr = request.form.get("sala")

        # Los profesores no pueden reservar el Sento
        if current_user.rango is Rango.PROFESOR and salaStr is "SENTO":
            print("Los profesores no pueden reservar el Sento")
            return redirect(url_for("nueva-reserva"))
        
        fecha = request.form.get("fecha")
        salaEnum = ""

        match salaStr:
            case "SENTO":
                salaEnum = Salas.SENTO
            case "AULA":
                salaEnum = Salas.AULA

        nuevaReserva = Reserva(
            id=ListaReservas.listaReservas.__len__() + 1,
            profesor=Usuario(
                current_user.id, current_user.nombre, current_user.email, 
                current_user.contraseña, current_user.rango
            ),
            sala=salaEnum,
            fecha=datetime.strptime(fecha, f"%Y-%m-%d").date()
        )

        ListaReservas.addReserva(nuevaReserva)
        print("Se ha creado una nueva mrseerva de {}".format(current_user.nombre))
        return redirect(url_for("rservas"))

    return render_template("reservas_form.html")

if __name__ == "__main__":
    app.run(debug=True)