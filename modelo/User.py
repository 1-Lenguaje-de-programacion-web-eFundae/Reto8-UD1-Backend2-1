from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from modelo.Rango import Rango


class Usuario(UserMixin):

    def __init__(self, id=0, nombre="", email="", password="", rango=Rango.NULL):
        if id != 0:
            self.id = id
            self.nombre = nombre
            self.email = email
            self.contraseña = generate_password_hash(password)
            self.rango = rango
        else:
            pass

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return '<Usuario {}>'.format(self.email)
    
  