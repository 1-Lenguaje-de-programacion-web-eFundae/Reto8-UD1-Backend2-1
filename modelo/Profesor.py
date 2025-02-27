from modelo.Rango import Rango
from werkzeug.security import generate_password_hash, check_password_hash

class Profesor:

    def __init__(self):
        self.nombre = self.email = self.contraseña = None
        self.rangoProfesor = Rango.Null

    def __init__(self, nombre, email, contraseña, rangoProfesor):
        self.nombre = nombre
        self.email = email
        self.contraseña = generate_password_hash(contraseña)
        self.rangoProfesor = rangoProfesor
    
    def check_password(self, contraseña : str):
        return check_password_hash(self.contraseña, contraseña)

    @staticmethod
    def getUser(email, profesores):
        for profesor in profesores:
            if profesor.email == email:
                return profesor
        return None

    def setNull(self):
        self.nombre = self.email = self.contraseña = ""
        self.rangoProfesor = Rango.Null

    def __str__(self):
        return f"'nombre': '{self.nombre}, 'email': '{self.email}', 'Rango': {self.rangoProfesor.__str__}"