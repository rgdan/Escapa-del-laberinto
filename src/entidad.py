# Entidad base para todos los objetos móviles en el mapa

class Entidad:
    def __init__(self, posicion): self.posicion = posicion
    def mover(self, nueva_posicion): self.posicion = nueva_posicion
