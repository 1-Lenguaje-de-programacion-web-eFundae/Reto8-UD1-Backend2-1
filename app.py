from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager
from modelo.Profesor import Profesor
from modelo.Rango import Rango

app = Flask(__name__)
app.secret_key = '1234'

login_manager = LoginManager()
login_manager.init_app(app)

profesores = [
    Profesor("Suzuki", "suzuki@boyobushido.jp", "1234", Rango.Sensei),
    Profesor("Shinnosuke", "shinnosuke@boyobushido.jp", "12345", Rango.Maestro),
    Profesor("Shigueru", "shigueru@boyobushido.jp", "123456", Rango.Profesor)
]

app.route("/")
def index():
    return "<h2>Bienvenido!</h2><br><a href='logon.html'>Crear usuario</a>"

# Creación de usuario
@app.route("/logon", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        rangoProfesor = Rango.Null
        
        match request.form['rangoProfesor']:
            case "Senséi":
                rangoProfesor = Rango.Sensei
            case "Maestro":
                rangoProfesor = Rango.Maestro
            case "Profesor":
                rangoProfesor = Rango.Profesor
            case _:
                rangoProfesor = Rango.Null

        profesorNuevo = Profesor(
            nombre=nombre, email=email, contraseña=contraseña, rangoProfesor=rangoProfesor
        )
        profesores.append(profesorNuevo)
        print("Profesor registrado correctamente: " + profesorNuevo.__str__)

        return redirect(url_for('index'))
    return render_template('logon.html')

# TO-DO: Login, Hacer reserva (Sento y Aula), Ver reservas

if __name__ == '__main__':
        app.run()