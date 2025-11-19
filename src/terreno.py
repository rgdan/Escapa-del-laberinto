class Terreno:
    def __init__(self, x, y):
        self.x = x  # fila
        self.y = y  # columna

    def es_accesible_jugador(self):
        return False

    def es_accesible_enemigo(self):
        return False


class Camino(Terreno):
    def es_accesible_jugador(self):
        return True

    def es_accesible_enemigo(self):
        return True


class Liana(Terreno):
    def es_accesible_enemigo(self):
        return True


class Tunel(Terreno):
    def es_accesible_jugador(self):
        return True


class Muro(Terreno):
    pass  # Ninguno puede pasar
