from entidad import Entidad

class Jugador(Entidad):
    def __init__(self, nombre , posicion):
        self.nombre = nombre
        super().__init__(posicion)
        self.energia = 100
        self.trampas = []
        self.max_trampas = 3
    
    def colocar_trampa(self):
        if len(self.trampas) < self.max_trampas:
            #colocar trampa en posicion actual
            pass