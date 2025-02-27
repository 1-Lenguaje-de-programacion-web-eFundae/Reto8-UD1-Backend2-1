from flask import Flask, redirect, render_template, request, url_for
from modelo.Profesor import Profesor
from modelo.Rango import Rango

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

profesores = [
    Profesor("Suzuki", "suzuki@boyobushido.jp", "1234", Rango.Sensei),
    Profesor("Shinnosuke", "shinnosuke@boyobushido.jp", "12345", Rango.Maestro),
    Profesor("Shigueru", "shigueru@boyobushido.jp", "123456", Rango.Profesor)
]

usuarioLogueado = Profesor("", "", "", Rango.Null)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

# Iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    global usuarioLogueado
    global profesores
    
    # Ya logueado
    if usuarioLogueado.email is not "" and request.method == "GET":
        return render_template('index.html')
   
    # Method POST
    if request.method == "POST":
        usuAux = Profesor.getUser(request.form.get("email"), profesores)
        if usuAux is not None and usuAux.check_password(request.form.get("contraseña")):
            usuarioLogueado = usuAux
            print("Profesor " + usuarioLogueado.nombre + " logueado")
            return redirect(url_for('index'))
    return render_template('login.html')
    

# Cerrar sesión
@app.route('/logout')
def logout():
    global usuarioLogueado
    if usuarioLogueado.email is not "": # Si hay usuario logueado
        print("Profesor " + usuarioLogueado.nombre + " ha cerrado sesión")
        usuarioLogueado.setNull()
    return redirect(url_for('index'))

# Creación de usuario
@app.route("/logon", methods=['GET', 'POST'])
def logon():
    global usuarioLogueado
    if usuarioLogueado.rangoProfesor is not Rango.Sensei:
        return redirect(url_for('index'))
    
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

        profesorNuevo = Profesor(nombre, email, contraseña, rangoProfesor)
        profesores.append(profesorNuevo)
        print("Profesor registrado correctamente: " + profesorNuevo.nombre)

        return redirect(url_for('index'))
    return render_template('logon.html')

# TO-DO: Login, Hacer reserva (Sento y Aula), Ver reservas

if __name__ == '__main__':
        app.run()