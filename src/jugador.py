import pygame
from src.entidad import Entidad

# player class
class Jugador(Entidad):
    def __init__(self, nombre, posicion, cell_size):
        self.nombre = nombre
        super().__init__(posicion)
        self.cell_size = cell_size
        
        self.sprints = 3
        self.max_sprints = 3
        self.sprint_recharge_time = 5.0
        self.time_since_sprint_used = 0
        
        self.sprint_active = False
        self.sprint_duration = 1.0
        self.sprint_timer = 0.0
        
        self.direction = 'down'
        self.is_moving = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        
        self._load_sprites()
        
    def _load_sprites(self):
        sprite_paths = [
            "sprites/protag/char_down_standing.png",
            "sprites/protag/char_down_walking_left.png",
            "sprites/protag/char_down_walking_right.png",
            "sprites/protag/char_left_standing.png",
            "sprites/protag/char_left_walking_1.png",
            "sprites/protag/char_left_walking_2.png",
            "sprites/protag/char_right_standing.png",
            "sprites/protag/char_right_walking_1.png",
            "sprites/protag/char_right_walking_2.png",
            "sprites/protag/char_up_standing.png",
            "sprites/protag/char_up_walking_left.png",
            "sprites/protag/char_up_walking_right.png",
        ]
        
        self.sprites = []
        for path in sprite_paths:
            sprite = pygame.image.load(path)
            sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
            self.sprites.append(sprite)
    
    # update sprinting and recharge 
    def update(self, dt, keys):
        if keys[pygame.K_LSHIFT] and self.sprints > 0 and not self.sprint_active:
            self.sprint_active = True
            self.sprint_timer = 0.0
            self.sprints -= 1
            self.time_since_sprint_used = 0
        
        if self.sprint_active:
            self.sprint_timer += dt
            if self.sprint_timer >= self.sprint_duration:
                self.sprint_active = False
                self.sprint_timer = 0.0
        
        if not self.sprint_active:
            self.time_since_sprint_used += dt
            if self.time_since_sprint_used >= self.sprint_recharge_time:
                if self.sprints < self.max_sprints:
                    self.sprints += 1
                    self.time_since_sprint_used = 0
    
    # update animation frames
    def update_animation(self, dt):
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame
        else:
            self.animation_frame = 0
            self.animation_timer = 0
    
    # attempt to move the player
    def try_move(self, nueva_fila, nueva_col, mapa):
        if nueva_fila < 0 or nueva_fila >= len(mapa): return False
        if nueva_col < 0 or nueva_col >= len(mapa[0]): return False
        
        terreno = mapa[nueva_fila][nueva_col]
        if not terreno.es_accesible_jugador(): return False
        
        self.posicion = (nueva_fila, nueva_col)
        self.is_moving = True
        
        return True
    
    # return current sprite based on movement and direction
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
