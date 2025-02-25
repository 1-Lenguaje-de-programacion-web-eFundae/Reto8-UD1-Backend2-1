from modelo.Rango import Rango

class Profesor:
    nombre = ""
    email = ""
    contraseña = ""
    rangoProfesor = Rango.Null

    def __init__(self, nombre, email, contraseña, rangoProfesor):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.rangoProfesor = rangoProfesor

    def __str__(self):
        return f"'nombre': '{self.nombre}, 'email': '{self.email}', 'Rango': {self.rangoProfesor.__str__}"