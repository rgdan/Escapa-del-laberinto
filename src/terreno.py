
# clase base Terreno
class Terreno:
    def __init__(self, x, y):
        self.x = x  # fila
        self.y = y  # columna

    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return False

# clases derivadas de Terreno

# Camino: accesible para jugador y enemigo
class Camino(Terreno):
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return True

# Liana: inaccesible para jugador, accesible para enemigo
class Liana(Terreno):
    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return True

# Tunel: accesible para jugador, inaccesible para enemigo
class Tunel(Terreno):
    def es_accesible_jugador(self): return True
    def es_accesible_enemigo(self): return False

# Muro: inaccesible para jugador y enemigo
class Muro(Terreno):
    def es_accesible_jugador(self): return False
    def es_accesible_enemigo(self): return False

# Trampa: accesible para jugador y enemigo, puede activarse una vez
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
