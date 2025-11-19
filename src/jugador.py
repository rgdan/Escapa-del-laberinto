class Jugador:
    def __init__(self, nombre , posicion):
        self.nombre = nombre
        self.posicion = posicion
        self.energia = 100
        self.trampas = []
        self.max_trampas = 3
    
    def mover(self, direccion):
        #logica para mover arriba, abajo, izquierda, derecha
        pass

    def colocar_trampa(self):
        if len(self.trampas) < self.max_trampas:
            #colocar trampa en posicion actual
            pass