from modelo.User import Usuario
from modelo.Rango import Rango

class ListaUsers:
      
    users = [
        Usuario(1, "Suzuki", "suzuki@boyobushido.jp", "1234", Rango.SENSEI)
    ]


    def addUser(self, usuario):
        self.users.append(usuario)
    
    def get_user(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None