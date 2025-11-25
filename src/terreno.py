class Terreno:
    def __init__(self, x, y):
        self.x = x  # fila
        self.y = y  # columna

    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return False

class Camino(Terreno):
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True

class Liana(Terreno):
    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return True

class Tunel(Terreno):
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return False

class Muro(Terreno):
    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return False

class Trampa(Terreno):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.activa = True
        
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True
    
    # activar la trampa
    def activar_trampa(self):
        if self.activa:
            self.activa = False
            return True
        return False
