from datetime import date
from modelo.Salas import Salas
from modelo.Reserva import Reserva
from modelo.ListaUsers import ListaUsers


class ListaReservas:

    listaReservas = [
        Reserva(1, ListaUsers.users[0], Salas.SENTO, date(2025, 2, 28))
    ]

    def addReserva(self, reserva : Reserva):
        self.listaReservas.append(reserva)