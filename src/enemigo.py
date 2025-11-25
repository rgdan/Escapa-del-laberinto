from src.entidad import Entidad
from collections import deque
import pygame
import random

# class for enemigo
class Enemigo(Entidad):
    def __init__(self, posicion, salidas=None):
        super().__init__(posicion)
        self.direction = 'down'
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.is_moving = False
        self.cell_size = 48
        
        # Asignar salida objetivo aleatoria para modo Cazador
        if salidas and len(salidas) > 0: self.target_exit = random.choice(salidas)
        else: self.target_exit = None
        
        self._load_sprites()
    
    def _load_sprites(self):
        sprite_paths = [
            "sprites/enemy/enemy_down_standing.png",
            "sprites/enemy/enemy_down_walking_left.png",
            "sprites/enemy/enemy_down_walking_right.png",
            "sprites/enemy/enemy_left_standing.png",
            "sprites/enemy/enemy_left_walking_1.png",
            "sprites/enemy/enemy_left_walking_2.png",
            "sprites/enemy/enemy_right_standing.png",
            "sprites/enemy/enemy_right_walking_1.png",
            "sprites/enemy/enemy_right_walking_2.png",
            "sprites/enemy/enemy_up_standing.png",
            "sprites/enemy/enemy_up_walking_left.png",
            "sprites/enemy/enemy_up_walking_right.png",
        ]
        
        # try to load sprites into list 
        self.sprites = []
        for path in sprite_paths:
            try:
                sprite = pygame.image.load(path)
                sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
                self.sprites.append(sprite)
            except:
                # Crear sprite de respaldo rojo
                sprite = pygame.Surface((self.cell_size, self.cell_size))
                sprite.fill((255, 0, 0))
                self.sprites.append(sprite)
    
    # get correct sprite based on direction and animation frame
    def get_current_sprite(self):
        if not self.is_moving:
            if self.direction == 'down': return self.sprites[0]
            elif self.direction == 'left': return self.sprites[3]
            elif self.direction == 'right': return self.sprites[6]
            elif self.direction == 'up': return self.sprites[9]
        
        if self.direction == 'down': return self.sprites[1] if self.animation_frame == 0 else self.sprites[2]
        elif self.direction == 'left': return self.sprites[4] if self.animation_frame == 0 else self.sprites[5]
        elif self.direction == 'right': return self.sprites[7] if self.animation_frame == 0 else self.sprites[8]
        elif self.direction == 'up': return self.sprites[10] if self.animation_frame == 0 else self.sprites[11]
        
        return self.sprites[0]
    
    # update enemy animation
    def update_animation(self, dt):
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame
        else:
            self.animation_frame = 0
            self.animation_timer = 0

    # update the way the enemy is facing dependiendo del movimiento
    def _actualizar_direccion(self, old_pos, new_pos):
        dx = new_pos[0] - old_pos[0]
        dy = new_pos[1] - old_pos[1]
        
        if dx > 0: self.direction = 'down'
        elif dx < 0: self.direction = 'up'
        elif dy > 0: self.direction = 'right'
        elif dy < 0: self.direction = 'left'

    # check if enemy is going to colide with jugador
    def colisiona_con(self, pos_jugador): return self.posicion[0] == pos_jugador[0] and self.posicion[1] == pos_jugador[1]

    # handle enemy behavior based on game mode
    def comportamiento_enemigo(self, modo, pos_jugador, mapa=None, salidas=None):
        self.is_moving = False
        old_pos = self.posicion.copy()
        nueva_pos = None
        
        if modo == "Escapa":
            # use bfs to try to find the best path
            if mapa: nueva_pos = self._encontrar_mejor_movimiento(pos_jugador, mapa)
            
            # just in case it doesnt work
            if not nueva_pos: nueva_pos = self._persecucion_simple_pos(pos_jugador, mapa)
        
        elif modo == "Cazador":
            # Ir directamente a la salida asignada
            if mapa and self.target_exit: nueva_pos = self._buscar_salida_inteligente([self.target_exit], mapa, pos_jugador)
            
            # Si no puede ir a la salida, huir del jugador
            if not nueva_pos: nueva_pos = self._huir_jugador_pos(pos_jugador, mapa)
        
        # Aplicar el movimiento solo si hay una posición válida
        if nueva_pos and nueva_pos != old_pos:
            self._actualizar_direccion(old_pos, nueva_pos)
            self.posicion = nueva_pos
            self.is_moving = True

    # chase the player using simple logic
    def _persecucion_simple_pos(self, pos_jugador, mapa):
        dx = pos_jugador[0] - self.posicion[0]
        dy = pos_jugador[1] - self.posicion[1]
        
        nueva_pos = self.posicion.copy()
        
        # Mover en x primero
        if dx > 0: nueva_pos[0] += 1
        elif dx < 0: nueva_pos[0] -= 1
        # Si no hay diferencia en x, mover en y
        elif dy > 0: nueva_pos[1] += 1
        elif dy < 0: nueva_pos[1] -= 1
        
        # Verificar si la nueva posición es válida
        if mapa and (0 <= nueva_pos[0] < len(mapa) and  0 <= nueva_pos[1] < len(mapa[0]) and mapa[nueva_pos[0]][nueva_pos[1]].es_accesible_enemigo()): return nueva_pos
        
        return None

    # use BFS to find the best movement towards the player
    def _encontrar_mejor_movimiento(self, pos_jugador, mapa):
        
        inicio = tuple(self.posicion)
        objetivo = tuple(pos_jugador)
        
        # Si ya estamos en el objetivo, no moverse
        if inicio == objetivo: return None
        
        # BFS para encontrar el camino más corto
        cola = deque([(inicio, [inicio])])
        visitados = {inicio}
        
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while cola:
            (row, col), camino = cola.popleft()
            
            # Explorar vecinos
            for dr, dc in direcciones:
                nueva_row, nueva_col = row + dr, col + dc
                nueva_pos = (nueva_row, nueva_col)
                
                # Verificar límites
                if (nueva_row < 0 or nueva_row >= len(mapa) or 
                    nueva_col < 0 or nueva_col >= len(mapa[0])):
                    continue
                
                # Verificar si ya visitamos esta posición
                if nueva_pos in visitados: continue
                
                # Verificar si el enemigo puede acceder a esta casilla
                if not mapa[nueva_row][nueva_col].es_accesible_enemigo(): continue
                
                visitados.add(nueva_pos)
                nuevo_camino = camino + [nueva_pos]
                
                # Si encontramos el objetivo, retornar el siguiente paso
                if nueva_pos == objetivo:
                    if len(nuevo_camino) > 1: return list(nuevo_camino[1])
                    return list(nueva_pos)
                
                cola.append((nueva_pos, nuevo_camino))
        
        # Si no hay camino, intentar acercarse directamente
        return self._movimiento_hacia_objetivo(pos_jugador, mapa)
    
    # try to move in tjhe most direct way towards the target
    def _movimiento_hacia_objetivo(self, pos_jugador, mapa):
        dx = pos_jugador[0] - self.posicion[0]
        dy = pos_jugador[1] - self.posicion[1]
        
        # Determinar prioridad de movimiento basado en distancia
        movimientos = []
        if abs(dx) >= abs(dy):
            # Priorizar movimiento en X
            if dx > 0: movimientos.append([self.posicion[0] + 1, self.posicion[1]])
            elif dx < 0: movimientos.append([self.posicion[0] - 1, self.posicion[1]])
            if dy > 0: movimientos.append([self.posicion[0], self.posicion[1] + 1])
            elif dy < 0: movimientos.append([self.posicion[0], self.posicion[1] - 1])
        else:
            # Priorizar movimiento en Y
            if dy > 0: movimientos.append([self.posicion[0], self.posicion[1] + 1])
            elif dy < 0: movimientos.append([self.posicion[0], self.posicion[1] - 1])
            if dx > 0: movimientos.append([self.posicion[0] + 1, self.posicion[1]])
            elif dx < 0: movimientos.append([self.posicion[0] - 1, self.posicion[1]])
        
        # Intentar cada movimiento en orden de prioridad
        for mov in movimientos:
            if (0 <= mov[0] < len(mapa) and 0 <= mov[1] < len(mapa[0]) and mapa[mov[0]][mov[1]].es_accesible_enemigo()): return mov
        
        return None

    # run away from the player
    def _huir_jugador_pos(self, pos_jugador, mapa):

        # Primero intentar huir usando BFS para encontrar el camino más lejano
        mejor_escape = self._encontrar_mejor_escape(pos_jugador, mapa)
        
        if mejor_escape: return mejor_escape
        
        # Si no hay escape por BFS, huir en dirección opuesta simple
        dx = pos_jugador[0] - self.posicion[0]
        dy = pos_jugador[1] - self.posicion[1]
        
        # Movimientos opuestos al jugador
        movimientos = []
        if abs(dx) >= abs(dy):
            if dx > 0: movimientos.append([self.posicion[0] - 1, self.posicion[1]])
            elif dx < 0: movimientos.append([self.posicion[0] + 1, self.posicion[1]])
            if dy > 0: movimientos.append([self.posicion[0], self.posicion[1] - 1])
            elif dy < 0: movimientos.append([self.posicion[0], self.posicion[1] + 1])
        else:
            if dy > 0: movimientos.append([self.posicion[0], self.posicion[1] - 1])
            elif dy < 0: movimientos.append([self.posicion[0], self.posicion[1] + 1])
            if dx > 0: movimientos.append([self.posicion[0] - 1, self.posicion[1]])
            elif dx < 0: movimientos.append([self.posicion[0] + 1, self.posicion[1]])
        
        # Intentar cada movimiento
        for mov in movimientos:
            if (0 <= mov[0] < len(mapa) and 0 <= mov[1] < len(mapa[0]) and mapa[mov[0]][mov[1]].es_accesible_enemigo()): return mov
        
        return None

    # find the best position to escape from the player
    def _encontrar_mejor_escape(self, pos_jugador, mapa):
        
        inicio = tuple(self.posicion)
        
        # Explorar posiciones vecinas y elegir la que maximice la distancia al jugador
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        mejor_posicion = None
        mejor_distancia = -1
        
        for dr, dc in direcciones:
            nueva_row = self.posicion[0] + dr
            nueva_col = self.posicion[1] + dc
            
            # Verificar límites
            if (nueva_row < 0 or nueva_row >= len(mapa) or nueva_col < 0 or nueva_col >= len(mapa[0])):
                continue
            
            # Verificar si el enemigo puede acceder
            if not mapa[nueva_row][nueva_col].es_accesible_enemigo(): continue
            
            # Calcular distancia Manhattan al jugador
            distancia = abs(nueva_row - pos_jugador[0]) + abs(nueva_col - pos_jugador[1])
            
            if distancia > mejor_distancia:
                mejor_distancia = distancia
                mejor_posicion = [nueva_row, nueva_col]
        
        return mejor_posicion

    # find the nearest exit avoiding the player
    def _buscar_salida(self, salidas, mapa, pos_jugador):
        
        # Encontrar la salida más cercana
        salida_mas_cercana = None
        distancia_minima = float('inf')
        
        for salida in salidas:
            distancia = abs(self.posicion[0] - salida[0]) + abs(self.posicion[1] - salida[1])
            if distancia < distancia_minima:
                distancia_minima = distancia
                salida_mas_cercana = salida
        
        if not salida_mas_cercana: return None
        
        # Usar BFS para encontrar el camino a la salida
        inicio = tuple(self.posicion)
        objetivo = tuple(salida_mas_cercana)
        
        # Si ya estamos en la salida
        if inicio == objetivo: return None
        
        # BFS para encontrar el camino más corto a la salida
        cola = deque([(inicio, [inicio])])
        visitados = {inicio}
        
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while cola:
            (row, col), camino = cola.popleft()
            
            # Explorar vecinos
            for dr, dc in direcciones:
                nueva_row, nueva_col = row + dr, col + dc
                nueva_pos = (nueva_row, nueva_col)
                
                # Verificar límites
                if (nueva_row < 0 or nueva_row >= len(mapa) or nueva_col < 0 or nueva_col >= len(mapa[0])): continue
                
                # Verificar si ya visitamos esta posición
                if nueva_pos in visitados: continue
                
                # Verificar si el enemigo puede acceder a esta casilla
                if not mapa[nueva_row][nueva_col].es_accesible_enemigo(): continue
                
                # Evitar la posición del jugador si está muy cerca
                distancia_jugador = abs(nueva_row - pos_jugador[0]) + abs(nueva_col - pos_jugador[1])

                # Si el jugador está muy cerca, intentar evitarlo
                if distancia_jugador <= 2: continue
                
                visitados.add(nueva_pos)
                nuevo_camino = camino + [nueva_pos]
                
                # Si encontramos la salida, retornar el siguiente paso
                if nueva_pos == objetivo:
                    if len(nuevo_camino) > 1: return list(nuevo_camino[1])
                    return list(nueva_pos)
                
                cola.append((nueva_pos, nuevo_camino))
        
        # Si no hay camino directo (jugador bloqueando), intentar huir primero
        mejor_escape = self._encontrar_mejor_escape(pos_jugador, mapa)
        if mejor_escape: return mejor_escape
        
        return None

    # intelligent exit search avoiding the player
    def _buscar_salida_inteligente(self, salidas, mapa, pos_jugador):

        # Encontrar todas las salidas accesibles con sus distancias
        salidas_accesibles = []
        for salida in salidas:
            distancia = abs(self.posicion[0] - salida[0]) + abs(self.posicion[1] - salida[1])
            salidas_accesibles.append((salida, distancia))
        
        # Ordenar salidas por distancia
        salidas_accesibles.sort(key=lambda x: x[1])
        
        # Intentar llegar a cada salida en orden de cercanía
        for salida, _ in salidas_accesibles:
            camino = self._buscar_camino_a_salida(salida, mapa, pos_jugador, evitar_jugador=True)
            if camino: return camino
        
        # Si no puede evitar al jugador, intentar sin evitarlo
        for salida, _ in salidas_accesibles:
            camino = self._buscar_camino_a_salida(salida, mapa, pos_jugador, evitar_jugador=False)
            if camino: return camino
        
        return None
    
    # search path to specific exit 
    def _buscar_camino_a_salida(self, salida, mapa, pos_jugador, evitar_jugador=True):

        inicio = tuple(self.posicion)
        objetivo = tuple(salida)
        
        # Si ya estamos en la salida
        if inicio == objetivo: return list(salida)
        
        # BFS para encontrar el camino más corto
        cola = deque([(inicio, [inicio])])
        visitados = {inicio}
        
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while cola:
            (row, col), camino = cola.popleft()
            
            # Explorar vecinos
            for dr, dc in direcciones:
                nueva_row, nueva_col = row + dr, col + dc
                nueva_pos = (nueva_row, nueva_col)
                
                # Verificar límites
                if (nueva_row < 0 or nueva_row >= len(mapa) or 
                    nueva_col < 0 or nueva_col >= len(mapa[0])):
                    continue
                
                # Verificar si ya visitamos esta posición
                if nueva_pos in visitados: continue
                
                # Verificar si el enemigo puede acceder a esta casilla
                if not mapa[nueva_row][nueva_col].es_accesible_enemigo(): continue
                
                # Evitar al jugador solo si está activado y muy cerca
                if evitar_jugador:
                    distancia_jugador = abs(nueva_row - pos_jugador[0]) + abs(nueva_col - pos_jugador[1])
                    if distancia_jugador <= 1:
                        # Skip esta posición si el jugador está demasiado cerca
                        continue
                
                visitados.add(nueva_pos)
                nuevo_camino = camino + [nueva_pos]
                
                # Si encontramos la salida, retornar el siguiente paso
                if nueva_pos == objetivo:
                    if len(nuevo_camino) > 1: return list(nuevo_camino[1])
                    return list(nueva_pos)
                
                cola.append((nueva_pos, nuevo_camino))
        
        return None