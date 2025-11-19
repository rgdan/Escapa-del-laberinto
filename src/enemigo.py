class Enemigo:
    def __init__(self, posicion):
        super().__init__(posicion)

    def mover(self,modo, pos_jugador):
        if modo == "Escapa":
            #perseguir jugador
            pass
        elif modo == "Cazador":
            #huir del jugador
            pass