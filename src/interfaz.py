import pygame
import sys
from src.jugador import Jugador
from src.terreno import Camino, Muro, Liana, Tunel

from src.enemigo import Enemigo

# class for text input field

class InputBox:
    def __init__(self, x, y, width, height, font, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = (163, 177, 138)
        self.color_active = (218, 215, 205)
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, (218, 215, 205))
        self.active = False
        self.bg_color = (52, 78, 65)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return 'submit'
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limitar longitud del nombre a 15 caracteres
                    if len(self.text) < 15:
                        self.text += event.unicode
                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, (218, 215, 205))
        return None
        
    def draw(self, screen):
        # Draw the background box
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 3, border_radius=5)
        # Draw the text
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        
    def get_text(self):
        return self.text.strip()

# class for making button

class Button:
    def __init__(self, x, y, width, height, text, action, color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.text_color = text_color
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (163, 177, 138), self.rect, 3, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos, mouse_click): return self.rect.collidepoint(mouse_pos) and mouse_click

# class for the main menu itself

class MainMenu:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Escapa del Laberinto")
        self.clock = pygame.time.Clock()
        
        # set colors - earthy palette
        self.BG_COLOR = (52, 78, 65)  # #344e41
        self.TITLE_COLOR = (218, 215, 205)  # #dad7cd
        self.BUTTON_COLOR = (88, 129, 87)  # #588157
        self.BUTTON_EXIT_COLOR = (58, 90, 64)  # #3a5a40
        self.TEXT_COLOR = (218, 215, 205)  # #dad7cd
        self.BORDER_COLOR = (163, 177, 138)  # #a3b18a
        
        # set fonts dynamically based on resolution
        self.title_font = pygame.font.Font(None, int(height * 0.133))
        self.button_font = pygame.font.Font(None, int(height * 0.067))
        
        # create buttons dynamically based on resolution
        button_width = int(width * 0.5)
        button_height = int(height * 0.08) 
        button_x = (width - button_width) // 2
        start_y = int(height * 0.25)
        spacing = int(height * 0.11)
        
        # list of buttons to create
        self.buttons = [
            Button(button_x, start_y, button_width, button_height, "Modo Escapa", "modo_escapa", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing, button_width, button_height, "Modo Cazador", "modo_cazador", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 2, button_width, button_height, "Leaderboard", "leaderboard", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 3, button_width, button_height, "Cómo Jugar", "como_jugar", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 4, button_width, button_height, "Dificultad", "dificultad", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 5, button_width, button_height, "Salir", "salir", self.BUTTON_EXIT_COLOR)
        ]
        
        self.running = True
        self.selected_option = None
        
    def draw(self):
        # draw background and title
        self.screen.fill(self.BG_COLOR)
        
        title_surface = self.title_font.render("Escapa del Laberinto", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_surface, title_rect)
        
        for button in self.buttons: button.draw(self.screen, self.button_font)
            
        pygame.display.flip()
        
    def interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.selected_option = 'quit'
                
            if event.type == pygame.MOUSEBUTTONDOWN: mouse_click = True
                
        # Verificar clicks en botones
        if mouse_click:
            for button in self.buttons:
                if button.is_clicked(mouse_pos, mouse_click):
                    self.selected_option = button.action
                    if button.action == 'salir': self.running = False
                        
    def run(self):
        # main loopsies
        while self.running:
            self.interactions()
            self.draw()
            self.clock.tick(60)
            
            # return selection option on button
            if self.selected_option and self.selected_option != 'salir': return self.selected_option
                
        return self.selected_option
    
# class for player tracking

class PlayerRegistration:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Registro de Jugador")
        self.clock = pygame.time.Clock()
        
        # Colors - same earthy palette
        self.BG_COLOR = (52, 78, 65)
        self.TITLE_COLOR = (218, 215, 205)
        self.BUTTON_COLOR = (88, 129, 87)
        self.TEXT_COLOR = (218, 215, 205)
        
        # Fonts
        self.title_font = pygame.font.Font(None, int(height * 0.1))
        self.text_font = pygame.font.Font(None, int(height * 0.05))
        self.button_font = pygame.font.Font(None, int(height * 0.067))
        
        # Input box
        input_width = int(width * 0.5)
        input_height = int(height * 0.08)
        input_x = (width - input_width) // 2
        input_y = int(height * 0.4)
        self.input_box = InputBox(input_x, input_y, input_width, input_height, self.text_font)
        
        # Continue button
        button_width = int(width * 0.3)
        button_height = int(height * 0.1)
        button_x = (width - button_width) // 2
        button_y = int(height * 0.6)
        self.continue_button = Button(button_x, button_y, button_width, button_height, "Continuar", "continue", self.BUTTON_COLOR)
        
        self.running = True
        self.player_name = None
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title_surface = self.title_font.render("Registro de Jugador", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, int(self.height * 0.15)))
        self.screen.blit(title_surface, title_rect)
        
        # Instruction text
        instruction = self.text_font.render("Ingresa tu nombre:", True, self.TEXT_COLOR)
        instruction_rect = instruction.get_rect(center=(self.width // 2, int(self.height * 0.3)))
        self.screen.blit(instruction, instruction_rect)
        
        # Input box
        self.input_box.draw(self.screen)
        
        # Continue button
        self.continue_button.draw(self.screen, self.button_font)
        
        pygame.display.flip()
        
    def interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN: mouse_click = True
                
            # Handle input box events
            result = self.input_box.handle_event(event)
            if result == 'submit' and self.input_box.get_text():
                self.player_name = self.input_box.get_text()
                self.running = False
                
        # Check continue button click
        if mouse_click and self.continue_button.is_clicked(mouse_pos, mouse_click):
            if self.input_box.get_text():
                self.player_name = self.input_box.get_text()
                self.running = False
                
    def run(self):
        while self.running:
            self.interactions()
            self.draw()
            self.clock.tick(60)
            
        return self.player_name

# class for leaderboard display

class Leaderboard:
    def __init__(self, width, height, score_manager):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tabla de Clasificación")
        self.clock = pygame.time.Clock()
        self.score_manager = score_manager
        
        # Colors
        self.BG_COLOR = (52, 78, 65)
        self.TITLE_COLOR = (218, 215, 205)
        self.SUBTITLE_COLOR = (163, 177, 138)
        self.TEXT_COLOR = (218, 215, 205)
        self.BUTTON_COLOR = (88, 129, 87)
        
        # Fonts
        self.title_font = pygame.font.Font(None, int(height * 0.1))
        self.subtitle_font = pygame.font.Font(None, int(height * 0.06))
        self.text_font = pygame.font.Font(None, int(height * 0.04))
        self.button_font = pygame.font.Font(None, int(height * 0.067))
        
        # Back button
        button_width = int(width * 0.3)
        button_height = int(height * 0.08)
        button_x = (width - button_width) // 2
        button_y = int(height * 0.88)
        self.back_button = Button(button_x, button_y, button_width, button_height, "Volver", "back", self.BUTTON_COLOR)
        
        self.running = True
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title_surface = self.title_font.render("Tabla de Clasificación", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, int(self.height * 0.08)))
        self.screen.blit(title_surface, title_rect)
        
        # Draw two columns for the two game modes
        col_width = self.width // 2
        
        # Modo Escapa (left column)
        self.draw_score_column("Top 5 - Modo Escapa", self.score_manager.get_scores('escapa'), 0, col_width)
        
        # Modo Cazador (right column)
        self.draw_score_column("Top 5 - Modo Cazador", self.score_manager.get_scores('cazador'), col_width, col_width)
        
        # Back button
        self.back_button.draw(self.screen, self.button_font)
        
        pygame.display.flip()

    # Draw a score column for a specific game mode  
    def draw_score_column(self, title, scores, x_offset, width):
        
        # Subtitle
        subtitle = self.subtitle_font.render(title, True, self.SUBTITLE_COLOR)
        subtitle_rect = subtitle.get_rect(center=(x_offset + width // 2, int(self.height * 0.18)))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Score entries
        start_y = int(self.height * 0.28)
        spacing = int(self.height * 0.08)
        
        if not scores:
            no_scores_text = self.text_font.render("No hay puntuaciones aún", True, self.TEXT_COLOR)
            no_scores_rect = no_scores_text.get_rect(center=(x_offset + width // 2, start_y + spacing))
            self.screen.blit(no_scores_text, no_scores_rect)
        else:
            for i in range(len(scores)):
                score_text = f"{i + 1}. {scores[i][0]} - {scores[i][1]} pts"
                score_surface = self.text_font.render(score_text, True, self.TEXT_COLOR)
                score_rect = score_surface.get_rect(center=(x_offset + width // 2, start_y + (i + 1) * spacing))
                self.screen.blit(score_surface, score_rect)
                
    def interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                
        # Check back button click
        if mouse_click and self.back_button.is_clicked(mouse_pos, mouse_click):
            self.running = False
            
    def run(self):
        while self.running:
            self.interactions()
            self.draw()
            self.clock.tick(60)

# class for difficulty selection

class DifficultySelection:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Selección de Dificultad")
        self.clock = pygame.time.Clock()
        
        # Colors - same earthy palette
        self.BG_COLOR = (52, 78, 65)
        self.TITLE_COLOR = (218, 215, 205)
        self.BUTTON_COLOR = (88, 129, 87)
        self.BUTTON_HARD_COLOR = (139, 69, 19)
        self.TEXT_COLOR = (218, 215, 205)
        
        # Fonts
        self.title_font = pygame.font.Font(None, int(height * 0.1))
        self.button_font = pygame.font.Font(None, int(height * 0.067))
        self.desc_font = pygame.font.Font(None, int(height * 0.04))
        
        # Buttons
        button_width = int(width * 0.5)
        button_height = int(height * 0.1)
        button_x = (width - button_width) // 2
        start_y = int(height * 0.25)
        spacing = int(height * 0.15)
        
        self.buttons = [
            Button(button_x, start_y, button_width, button_height, "Fácil", "facil", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing, button_width, button_height, "Normal", "normal", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 2, button_width, button_height, "Difícil", "dificil", self.BUTTON_HARD_COLOR),
            Button(button_x, start_y + spacing * 3, button_width, button_height, "Volver", "back", self.BUTTON_COLOR)
        ]
        
        # Difficulty descriptions
        self.descriptions = {
            "facil": "Enemigos lentos - Ideal para principiantes",
            "normal": "Velocidad estándar - Desafío equilibrado",
            "dificil": "Enemigos rápidos - Solo para expertos"
        }
        
        self.running = True
        self.selected_difficulty = None
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        title = self.title_font.render("Selecciona Dificultad", True, self.TITLE_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, int(self.height * 0.1)))
        self.screen.blit(title, title_rect)
        
        # Draw buttons with descriptions
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons[:-1]):  # Exclude back button
            button.draw(self.screen, self.button_font)
            
            # Show description on hover
            if button.rect.collidepoint(mouse_pos):
                desc_text = self.desc_font.render(self.descriptions[button.action], True, self.TEXT_COLOR)
                desc_rect = desc_text.get_rect(center=(self.width // 2, button.rect.bottom + 25))
                self.screen.blit(desc_text, desc_rect)
        
        # Draw back button
        self.buttons[-1].draw(self.screen, self.button_font)
        
        pygame.display.flip()
        
    def interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.selected_difficulty = None
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                self.selected_difficulty = None
                
        if mouse_click:
            for button in self.buttons:
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.action == 'back':
                        self.running = False
                        self.selected_difficulty = None
                    else:
                        self.selected_difficulty = button.action
                        self.running = False
                        
    def run(self):
        while self.running:
            self.interactions()
            self.draw()
            self.clock.tick(60)
            
        return self.selected_difficulty

# class for how to play screen

class HowToPlay:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Cómo Jugar")
        self.clock = pygame.time.Clock()
        
        self.BG_COLOR = (52, 78, 65)
        self.TITLE_COLOR = (218, 215, 205)
        self.TEXT_COLOR = (218, 215, 205)
        self.SUBTITLE_COLOR = (163, 177, 138)
        self.BUTTON_COLOR = (88, 129, 87)
        
        self.title_font = pygame.font.Font(None, int(height * 0.08))
        self.subtitle_font = pygame.font.Font(None, int(height * 0.05))
        self.text_font = pygame.font.Font(None, int(height * 0.03))
        self.button_font = pygame.font.Font(None, int(height * 0.067))
        
        button_width = int(width * 0.25)
        button_height = int(height * 0.08)
        button_x = (width - button_width) // 2
        button_y = int(height * 0.92)
        self.back_button = Button(button_x, button_y, button_width, button_height, "Volver", "back", self.BUTTON_COLOR)
        
        self.tile_size = 32
        self.texture_camino = pygame.transform.scale(pygame.image.load("sprites/background/camino.png"), (self.tile_size, self.tile_size))
        self.texture_muro = pygame.transform.scale(pygame.image.load("sprites/background/muro.png"), (self.tile_size, self.tile_size))
        self.texture_lianas = pygame.transform.scale(pygame.image.load("sprites/background/lianas.png"), (self.tile_size, self.tile_size))
        self.texture_tunel = pygame.transform.scale(pygame.image.load("sprites/background/tunel.png"), (self.tile_size, self.tile_size))
        
        self.running = True
        
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        
        title = self.title_font.render("Cómo Jugar", True, self.TITLE_COLOR)
        title_rect = title.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title, title_rect)
        
        y_pos = 90
        
        subtitle = self.subtitle_font.render("Modos de Juego:", True, self.SUBTITLE_COLOR)
        self.screen.blit(subtitle, (50, y_pos))
        y_pos += 40
        
        modes_text = [
            "Modo Escapa: Encuentra la salida antes de que te alcance el enemigo(Puedes utilizar trampas para deshacerte de los enemigos)",
            "Modo Cazador: Elimina al enemigo colisionando contra él, evita que llegue a la salida"
        ]
        for text in modes_text:
            line = self.text_font.render(text, True, self.TEXT_COLOR)
            self.screen.blit(line, (70, y_pos))
            y_pos += 30
        
        y_pos += 20
        subtitle = self.subtitle_font.render("Controles:", True, self.SUBTITLE_COLOR)
        self.screen.blit(subtitle, (50, y_pos))
        y_pos += 40
        
        controls_text = [
            "WASD o Flechas: Mover jugador",
            "Shift Izquierdo: Correr (consume energía)",
            "Espacio: Colocar trampa (modo Escapa)",
            "ESC: Salir del juego"
        ]
        for text in controls_text:
            line = self.text_font.render(text, True, self.TEXT_COLOR)
            self.screen.blit(line, (70, y_pos))
            y_pos += 30
        
        y_pos += 20
        subtitle = self.subtitle_font.render("Terrenos:", True, self.SUBTITLE_COLOR)
        self.screen.blit(subtitle, (50, y_pos))
        y_pos += 40
        
        camino = Camino(0, 0)
        muro = Muro(0, 0)
        liana = Liana(0, 0)
        tunel = Tunel(0, 0)
        
        terrenos = [
            (self.texture_camino, "Camino", camino),
            (self.texture_muro, "Muro", muro),
            (self.texture_lianas, "Lianas", liana),
            (self.texture_tunel, "Túnel", tunel)
        ]
        
        for texture, name, terreno in terrenos:
            self.screen.blit(texture, (70, y_pos))
            
            name_text = self.text_font.render(f"{name}:", True, self.TEXT_COLOR)
            self.screen.blit(name_text, (115, y_pos + 5))
            
            player_access = "Sí" if terreno.es_accesible_jugador() else "No"
            enemy_access = "Sí" if terreno.es_accesible_enemigo() else "No"
            
            access_text = self.text_font.render(
                f"Jugador: {player_access} | Enemigo: {enemy_access}", 
                True, self.TEXT_COLOR
            )
            self.screen.blit(access_text, (250, y_pos + 5))
            
            y_pos += 45
        
        self.back_button.draw(self.screen, self.button_font)
        pygame.display.flip()
        
    def interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                
        if mouse_click and self.back_button.is_clicked(mouse_pos, mouse_click):
            self.running = False
            
    def run(self):
        while self.running:
            self.interactions()
            self.draw()
            self.clock.tick(60)

# class for the game window

class GameWindow:
    #E: mapa (list), title (str), width (int), height (int), cell_size (int), player_name (str), inicio (tuple), modo (str), salidas (list of tuples), dificultad (str)
    #S: GameWindow instance
    def __init__(self, mapa, title, width, height, cell_size, player_name, inicio, modo, salidas, dificultad='normal'):
        pygame.init()
        self.mapa = mapa
        self.title = title
        self.rows = len(mapa)
        self.cols = len(mapa[0]) 

        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        self.modo = modo
        self.salidas = salidas
        self.dificultad = dificultad
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_won = False
        self.game_over = False
        
        self.game_time = 0.0
        self.final_score = 0
        
        # Time limit para Modo Cazador según dificultad
        if modo == 'modo_cazador':
            if dificultad == 'facil':
                self.time_limit = 120.0  # 2 minutos
            elif dificultad == 'normal':
                self.time_limit = 60.0  # 1 minuto
            elif dificultad == 'dificil':
                self.time_limit = 25.0   # 25 segundos
            else:
                self.time_limit = 120.0  # default 2 minutos
        else:
            self.time_limit = None  # Sin límite en Modo Escapa

        # Cargar texturas con manejo de errores
        try:
            self.texture_camino = pygame.image.load("sprites/background/camino.png")
            self.texture_muro = pygame.image.load("sprites/background/muro.png")
            self.texture_tunel = pygame.image.load("sprites/background/tunel.png")
            self.texture_lianas = pygame.image.load("sprites/background/lianas.png")
        except:
            # Crear texturas de color si no existen los archivos
            self.texture_camino = pygame.Surface((cell_size, cell_size))
            self.texture_camino.fill((200, 200, 200))
            self.texture_muro = pygame.Surface((cell_size, cell_size))
            self.texture_muro.fill((50, 50, 50))
            self.texture_tunel = pygame.Surface((cell_size, cell_size))
            self.texture_tunel.fill((100, 100, 200))
            self.texture_lianas = pygame.Surface((cell_size, cell_size))
            self.texture_lianas.fill((0, 150, 0))
        
        self.texture_camino = pygame.transform.scale(self.texture_camino, (self.cell_size, self.cell_size))
        self.texture_muro = pygame.transform.scale(self.texture_muro, (self.cell_size, self.cell_size))
        self.texture_tunel = pygame.transform.scale(self.texture_tunel, (self.cell_size, self.cell_size))
        self.texture_lianas = pygame.transform.scale(self.texture_lianas, (self.cell_size, self.cell_size))

        try:
            self.energy_icon = pygame.image.load("sprites/energy/energy.png")
            self.energy_icon = pygame.transform.scale(self.energy_icon, (30, 30))
        except:
            self.energy_icon = pygame.Surface((30, 30))
            self.energy_icon.fill((255, 255, 0))
        
        # Cargar sprite de trampa
        try:
            self.trap_sprite = pygame.image.load("sprites/trap/trap.png")
            self.trap_sprite = pygame.transform.scale(self.trap_sprite, (self.cell_size, self.cell_size))
        except:
            # Crear sprite de respaldo si no existe
            self.trap_sprite = pygame.Surface((self.cell_size, self.cell_size))
            self.trap_sprite.fill((255, 0, 0))
            # Dibujar círculo en el sprite de respaldo
            pygame.draw.circle(self.trap_sprite, (200, 0, 0), (self.cell_size // 2, self.cell_size // 2), self.cell_size // 4)
        
        pygame.mixer.init()
        try:
            self.sprint_sound = pygame.mixer.Sound("sounds/sprint.mp3")
        except:
            self.sprint_sound = None
        
        try:
            self.victory_sound = pygame.mixer.Sound("sounds/victory.mp3")
        except:
            self.victory_sound = None
        
        try:
            self.death_sound = pygame.mixer.Sound("sounds/death.mp3")
        except:
            self.death_sound = None
        
        try:
            self.defeat_sound = pygame.mixer.Sound("sounds/defeat.mp3")
        except:
            self.defeat_sound = None

        self.color_bg = (34, 139, 34)
        self.color_grid = (0, 0, 0)
        self.color_text = (255, 255, 255)

        self.grid_w = self.cols * self.cell_size
        self.grid_h = self.rows * self.cell_size
        self.offset_x = (self.width - self.grid_w) // 2
        self.offset_y = (self.height - self.grid_h) // 2
        
        self.player = Jugador(player_name, inicio, cell_size)
        
        # Inicializar enemigos
        self.enemigos = []
        self.enemigo_move_cooldown = 0
        
        # Ajustar velocidad de enemigos según dificultad
        if dificultad == 'facil':
            self.enemigo_move_delay = 0.9  # Más lento
        elif dificultad == 'normal':
            self.enemigo_move_delay = 0.6  # Velocidad estándar
        elif dificultad == 'dificil':
            self.enemigo_move_delay = 0.3  # Más rápido
        else:
            self.enemigo_move_delay = 0.6  # Por defecto
        
        # Variables para trampas (solo modo Escapa)
        self.trampas = []
        self.max_trampas = 5
        self.trampas_colocadas = 0
        self.enemigos_eliminados = 0
        
        # Variables adicionales para modo Cazador
        self.enemigos_escapados = 0
        self.penalty_score = 0
        self.bonus_score = 0
        
        self.spawn_enemigos()
        
        self.font = pygame.font.Font(None, 36)
        
        self.move_cooldown = 0
        self.move_delay = 0.45
        self.sprint_sound_played = False

    #E: None
    #S: None
    def draw_grid(self):
        self.screen.fill(self.color_bg)
        for x in range(self.rows):
            for y in range(self.cols):
                terreno = self.mapa[x][y]
                pos_x = self.offset_x + y * self.cell_size
                pos_y = self.offset_y + x * self.cell_size
                
                if isinstance(terreno, Camino):
                    texture = self.texture_camino
                elif isinstance(terreno, Muro):
                    texture = self.texture_muro
                elif isinstance(terreno, Liana):
                    texture = self.texture_lianas
                elif isinstance(terreno, Tunel):
                    texture = self.texture_tunel
                else:
                    texture = self.texture_muro
                
                self.screen.blit(texture, (pos_x, pos_y))
                
                rect = pygame.Rect(pos_x, pos_y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.color_grid, rect, 1)
    
    #E: None
    #S: None
    def draw_player(self):
        player_row, player_col = self.player.posicion
        pos_x = self.offset_x + player_col * self.cell_size
        pos_y = self.offset_y + player_row * self.cell_size
        
        sprite = self.player.get_current_sprite()
        self.screen.blit(sprite, (pos_x, pos_y))
    
    # Dibujar enemigos
    def draw_enemigos(self):
        for enemigo in self.enemigos:
            enemy_row, enemy_col = enemigo.posicion
            pos_x = self.offset_x + enemy_col * self.cell_size
            pos_y = self.offset_y + enemy_row * self.cell_size
            sprite = enemigo.get_current_sprite()
            self.screen.blit(sprite, (pos_x, pos_y))

    #E: None
    #S: None
    def draw_ui(self):
        ui_x = 10
        ui_y = 10
        
        self.screen.blit(self.energy_icon, (ui_x, ui_y))
        
        sprint_text = self.font.render(f"x {self.player.sprints}", True, self.color_text)
        self.screen.blit(sprint_text, (ui_x + 40, ui_y))
        
        if self.player.sprint_active:
            time_remaining = self.player.sprint_duration - self.player.sprint_timer
            boost_text = self.font.render(f"BOOST: {time_remaining:.1f}s", True, (255, 255, 0))
            self.screen.blit(boost_text, (ui_x + 120, ui_y))
        elif self.player.sprints < self.player.max_sprints:
            recharge_progress = self.player.time_since_sprint_used / self.player.sprint_recharge_time
            bar_width = 100
            bar_height = 10
            bar_x = ui_x + 120
            bar_y = ui_y + 10
            
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * recharge_progress), bar_height))
        
        # UI adicional para modo Escapa (con trampas)
        if self.modo == 'modo_escapa':
            trap_y = ui_y + 50
            trampas_restantes = self.max_trampas - self.trampas_colocadas
            trap_text = self.font.render(f"Trampas: {trampas_restantes}/{self.max_trampas}", True, self.color_text)
            self.screen.blit(trap_text, (ui_x, trap_y))
            
            enemies_text = self.font.render(f"Enemigos: {len(self.enemigos)}", True, self.color_text)
            self.screen.blit(enemies_text, (ui_x, trap_y + 40))
        
        # UI adicional para modo Cazador
        elif self.modo == 'modo_cazador':
            enemies_y = ui_y + 50
            
            # Mostrar tiempo restante
            if self.time_limit:
                time_remaining = max(0, self.time_limit - self.game_time)
                minutes = int(time_remaining // 60)
                seconds = int(time_remaining % 60)
                time_color = (255, 255, 255) if time_remaining > 30 else (255, 0, 0)
                timer_text = self.font.render(f"Tiempo: {minutes}:{seconds:02d}", True, time_color)
                self.screen.blit(timer_text, (ui_x, enemies_y))
                enemies_y += 40
            
            # Mostrar enemigos capturados
            captured_text = self.font.render(f"Capturados: {self.enemigos_eliminados}", True, (0, 255, 0))
            self.screen.blit(captured_text, (ui_x, enemies_y))
            
            # Mostrar enemigos escapados
            escaped_text = self.font.render(f"Escapados: {self.enemigos_escapados}", True, (255, 100, 100))
            self.screen.blit(escaped_text, (ui_x, enemies_y + 35))
            
            # Mostrar puntuación actual
            current_score = self.calculate_score()
            score_text = self.font.render(f"Puntos: {current_score}", True, (255, 215, 0))
            self.screen.blit(score_text, (ui_x, enemies_y + 70))

    # ...existing code...

    def draw_win_message(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        win_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 28)
        
        if self.modo == 'modo_escapa':
            win_text = win_font.render("¡GANASTE!", True, (255, 215, 0))
        else:  # modo_cazador
            win_text = win_font.render("TIEMPO AGOTADO", True, (255, 215, 0))
        
        win_rect = win_text.get_rect(center=(self.width // 2, self.height // 2 - 120))
        self.screen.blit(win_text, win_rect)
        
        if self.modo == 'modo_escapa':
            time_text = subtitle_font.render(f"Tiempo: {self.game_time:.1f}s", True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            self.screen.blit(time_text, time_rect)
            
            score_text = subtitle_font.render(f"Puntuación: {self.final_score}", True, (255, 215, 0))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            self.screen.blit(score_text, score_rect)
        elif self.modo == 'modo_cazador':
            time_text = subtitle_font.render(f"Tiempo: {self.game_time:.1f}s", True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(self.width // 2, self.height // 2 - 60))
            self.screen.blit(time_text, time_rect)
            
            # Estadísticas
            captured_text = small_font.render(f"Enemigos capturados: {self.enemigos_eliminados} (+{self.bonus_score} pts)", True, (0, 255, 0))
            captured_rect = captured_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            self.screen.blit(captured_text, captured_rect)
            
            escaped_text = small_font.render(f"Enemigos escapados: {self.enemigos_escapados} ({self.penalty_score} pts)", True, (255, 100, 100))
            escaped_rect = escaped_text.get_rect(center=(self.width // 2, self.height // 2 + 10))
            self.screen.blit(escaped_text, escaped_rect)
            
            score_text = subtitle_font.render(f"Puntuación Final: {self.final_score}", True, (255, 215, 0))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(score_text, score_rect)
        
        press_esc_text = subtitle_font.render("Presiona ESC para volver al menú", True, (255, 255, 255))
        press_esc_rect = press_esc_text.get_rect(center=(self.width // 2, self.height // 2 + 120))
        self.screen.blit(press_esc_text, press_esc_rect)

    def check_win_condition(self):
        if self.modo == 'modo_escapa':
            player_pos = self.player.posicion
            if player_pos in self.salidas:
                return True
        

    def calculate_score(self):
        if self.modo == 'modo_escapa':
            intervals = int(self.game_time / 5.0)
            score = 1000 - (intervals * 100)
            return max(score, 0)
        elif self.modo == 'modo_cazador':
            # Puntuación comienza en 0
            base_score = 0
            
            # Bonificación por enemigos capturados (+200 por cada uno)
            capture_bonus = self.enemigos_eliminados * 200
            self.bonus_score = capture_bonus
            
            # Penalización por enemigos escapados (-150 por cada uno)
            escape_penalty = self.enemigos_escapados * 100
            self.penalty_score = -escape_penalty
            
            # Penalización por tiempo (más suave) - solo se aplica al final
            #time_penalty = int(self.game_time / 5.0) * 30
            
            # Puntuación final
            score = base_score + capture_bonus - escape_penalty 
            return max(score, 0)
        return 0
    
    #E: None
    #S: None
    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()
        
        was_sprinting = self.player.sprint_active
        self.player.update(dt, keys)
        
        if self.player.sprint_active and not was_sprinting and self.sprint_sound:
            self.sprint_sound.play()
            self.sprint_sound_played = True
        elif not self.player.sprint_active:
            self.sprint_sound_played = False
        
        if self.move_cooldown > 0:
            self.move_cooldown -= dt
            self.player.update_animation(dt)
            return
        
        self.player.is_moving = False
        
        player_row, player_col = self.player.posicion
        moved = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.direction = 'up'
            moved = self.player.try_move(player_row - 1, player_col, self.mapa)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.direction = 'down'
            moved = self.player.try_move(player_row + 1, player_col, self.mapa)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.direction = 'left'
            moved = self.player.try_move(player_row, player_col - 1, self.mapa)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.direction = 'right'
            moved = self.player.try_move(player_row, player_col + 1, self.mapa)
        
        self.player.update_animation(dt)
        
        if moved:
            if self.player.sprint_active:
                self.move_cooldown = self.move_delay / 3
            else:
                self.move_cooldown = self.move_delay

    # Spawn enemigos en posiciones válidas alejadas del jugador
    def spawn_enemigos(self):
        import random
        num_enemigos = 3 if self.modo == 'modo_escapa' else 3
        
        for _ in range(num_enemigos):
            attempts = 0
            while attempts < 200:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                
                # Verificar que la posición sea válida y esté lejos del jugador
                if (isinstance(self.mapa[row][col], Camino) and 
                    [row, col] != self.player.posicion and
                    abs(row - self.player.posicion[0]) + abs(col - self.player.posicion[1]) > 10):
                    self.enemigos.append(Enemigo([row, col], self.salidas))
                    break
                attempts += 1

    #E: None
    #S: None
    def loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE and self.modo == 'modo_escapa':
                        # Colocar trampa en modo Escapa
                        if not self.game_won and not self.game_over:
                            self.colocar_trampa()
            
            if not self.game_won and not self.game_over:
                self.game_time += dt
                
                # Verificar límite de tiempo en Modo Cazador
                if self.modo == 'modo_cazador' and self.time_limit:
                    if self.game_time >= self.time_limit:
                        self.game_won = True
                        self.final_score = self.calculate_score()
                
                self.handle_movement(dt)
                self.move_enemigos(dt)
                
                if self.modo == 'modo_escapa':
                    # Modo Escapa: game over si te toca un enemigo
                    if self.check_enemy_collision():
                        self.game_over = True
                        if self.defeat_sound:
                            self.defeat_sound.play()
                    if self.check_win_condition():
                        self.game_won = True
                        if self.victory_sound:
                            self.victory_sound.play()
                    
                    # Verificar trampas
                    self.check_trampa_colision()
                
                elif self.modo == 'modo_cazador':
                    # Modo Cazador: eliminas enemigos al tocarlos
                    if self.check_enemy_collision():
                        self.eliminar_enemigo_tocado()
                    
                    # Verificar si algún enemigo escapó y generar uno nuevo
                    self.check_enemy_escape()
            
            self.draw_grid()
            if self.modo == 'modo_escapa':
                self.draw_trampas()
            self.draw_enemigos()
            self.draw_player()
            self.draw_ui()
            
            if self.game_won:
                self.draw_win_message()
            elif self.game_over:
                self.draw_game_over_message()
            
            pygame.display.flip()

    # Verificar colisiones con enemigos
    def check_enemy_collision(self):
        for enemigo in self.enemigos:
            if enemigo.colisiona_con(self.player.posicion):
                return True
        return False
    
    def eliminar_enemigo_tocado(self):
        """Eliminar enemigo que tocó el jugador en modo Cazador"""
        enemigos_a_eliminar = []
        
        for i, enemigo in enumerate(self.enemigos):
            if enemigo.colisiona_con(self.player.posicion):
                enemigos_a_eliminar.append(i)
        
        # Eliminar enemigos en orden inverso
        for i in sorted(enemigos_a_eliminar, reverse=True):
            del self.enemigos[i]
            self.enemigos_eliminados += 1
            
            if self.death_sound:
                self.death_sound.play()
            
            # Generar nuevo enemigo por cada uno capturado
            self.spawn_nuevo_enemigo()

    # Mover enemigos
    def move_enemigos(self, dt):
        # Actualizar animaciones de todos los enemigos
        for enemigo in self.enemigos:
            enemigo.update_animation(dt)
        
        if self.enemigo_move_cooldown > 0:
            self.enemigo_move_cooldown -= dt
            return
        
        # Recopilar todas las posiciones actuales de enemigos
        enemigo_positions = set()
        for enemigo in self.enemigos:
            enemigo_positions.add(tuple(enemigo.posicion))
        
        for enemigo in self.enemigos:
            old_pos = enemigo.posicion.copy()
            
            if self.modo == 'modo_escapa':
                # Modo Escapa: enemigos persiguen al jugador
                enemigo.comportamiento_enemigo('Escapa', self.player.posicion, self.mapa)
            else:
                # Modo Cazador: enemigos buscan la salida evitando al jugador
                enemigo.comportamiento_enemigo('Cazador', self.player.posicion, self.mapa, self.salidas)
            
            # Verificar si la nueva posición es válida
            new_row, new_col = enemigo.posicion
            new_pos = (new_row, new_col)
            
            # Si la posición es inválida, revertir
            if (new_row < 0 or new_row >= self.rows or 
                new_col < 0 or new_col >= self.cols):
                enemigo.posicion = old_pos
                enemigo.is_moving = False
            elif not self.mapa[new_row][new_col].es_accesible_enemigo():
                enemigo.posicion = old_pos
                enemigo.is_moving = False
            elif new_pos != tuple(old_pos) and new_pos in enemigo_positions:
                # Si otro enemigo ya está en esta posición, revertir
                enemigo.posicion = old_pos
                enemigo.is_moving = False
            else:
                # Actualizar el conjunto de posiciones
                enemigo_positions.discard(tuple(old_pos))
                enemigo_positions.add(new_pos)
        
        self.enemigo_move_cooldown = self.enemigo_move_delay

    # Dibujar mensaje de derrota
    def draw_game_over_message(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 28)
        
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        if self.modo == 'modo_escapa':
            death_text = subtitle_font.render("¡Te atrapó el enemigo!", True, (255, 255, 255))
            death_rect = death_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            self.screen.blit(death_text, death_rect)

            score_text = subtitle_font.render(f"Puntuación: {self.final_score}", True, (255, 215, 0))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            self.screen.blit(score_text, score_rect)
        else:  # modo_cazador
            # Verificar si perdió por tiempo o por enemigos escapados
            if self.time_limit and self.game_time >= self.time_limit:
                death_text = subtitle_font.render("¡Se acabó el tiempo!", True, (255, 255, 255))
            else:
                death_text = subtitle_font.render("¡Todos los enemigos escaparon!", True, (255, 255, 255))
            death_rect = death_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
            self.screen.blit(death_text, death_rect)
            
            # Mostrar estadísticas finales
            final_score = self.calculate_score()
            
            captured_text = small_font.render(f"Enemigos capturados: {self.enemigos_eliminados} (+{self.bonus_score} pts)", True, (0, 255, 0))
            captured_rect = captured_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(captured_text, captured_rect)
            
            escaped_text = small_font.render(f"Enemigos escapados: {self.enemigos_escapados} ({self.penalty_score} pts)", True, (255, 100, 100))
            escaped_rect = escaped_text.get_rect(center=(self.width // 2, self.height // 2 + 30))
            self.screen.blit(escaped_text, escaped_rect)
            
            score_text = subtitle_font.render(f"Puntuación Final: {final_score}", True, (255, 215, 0))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
            self.screen.blit(score_text, score_rect)
        
        press_esc_text = subtitle_font.render("Presiona ESC para volver al menú", True, (255, 255, 255))
        press_esc_rect = press_esc_text.get_rect(center=(self.width // 2, self.height // 2 + 120))
        self.screen.blit(press_esc_text, press_esc_rect)

    def colocar_trampa(self):
        """Coloca una trampa en la posición actual del jugador"""
        if self.trampas_colocadas >= self.max_trampas:
            return False
        
        player_pos = tuple(self.player.posicion)
        
        # Verificar que no haya ya una trampa en esta posición
        for trampa_pos in self.trampas:
            if trampa_pos == player_pos:
                return False
        
        # Colocar la trampa
        self.trampas.append(player_pos)
        self.trampas_colocadas += 1
        return True

    def draw_trampas(self):
        """Dibujar las trampas en el mapa usando sprites"""
        for trampa_pos in self.trampas:
            row, col = trampa_pos
            pos_x = self.offset_x + col * self.cell_size
            pos_y = self.offset_y + row * self.cell_size
            
            # Dibujar sprite de trampa
            self.screen.blit(self.trap_sprite, (pos_x, pos_y))

    def check_trampa_colision(self):
        """Verificar si algún enemigo cayó en una trampa (solo modo Escapa)"""
        enemigos_a_eliminar = []
        trampas_a_eliminar = []
        
        for i, enemigo in enumerate(self.enemigos):
            enemigo_pos = tuple(enemigo.posicion)
            if enemigo_pos in self.trampas:
                enemigos_a_eliminar.append(i)
                if enemigo_pos not in trampas_a_eliminar:
                    trampas_a_eliminar.append(enemigo_pos)
        
        # Eliminar trampas usadas (verificando que existan primero)
        for trampa_pos in trampas_a_eliminar:
            if trampa_pos in self.trampas:
                self.trampas.remove(trampa_pos)
        
        # Eliminar enemigos en orden inverso para no afectar índices
        for i in sorted(enemigos_a_eliminar, reverse=True):
            del self.enemigos[i]
            self.enemigos_eliminados += 1
            if self.death_sound:
                self.death_sound.play()

    #E: None
    #S: int or None
    def get_final_score(self):
        """Retorna la puntuación final si el juego fue ganado"""
        if self.game_won:
            return self.final_score
        return None
    
    #E: None
    #S: str
    def get_player_name(self):
        """Retorna el nombre del jugador"""
        return self.player.nombre

    def check_enemy_escape(self):
        """Verificar si algún enemigo llegó a la salida en modo Cazador"""
        enemigos_escapados = []
        
        for i, enemigo in enumerate(self.enemigos):
            enemigo_pos = tuple(enemigo.posicion)
            if enemigo_pos in [tuple(s) for s in self.salidas]:
                enemigos_escapados.append(i)
        
        # Si al menos un enemigo escapó
        if enemigos_escapados:
            # Eliminar enemigos que escaparon en orden inverso
            for i in sorted(enemigos_escapados, reverse=True):
                del self.enemigos[i]
                self.enemigos_escapados += 1
                
                # Generar nuevo enemigo por cada uno que escapó
                self.spawn_nuevo_enemigo()
    
    def spawn_nuevo_enemigo(self):
        """Generar un nuevo enemigo en posición aleatoria alejada del jugador"""
        import random
        
        attempts = 0
        while attempts < 200:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # Verificar que la posición sea válida y esté lejos del jugador
            if (isinstance(self.mapa[row][col], Camino) and 
                [row, col] != self.player.posicion and
                abs(row - self.player.posicion[0]) + abs(col - self.player.posicion[1]) > 10):
                self.enemigos.append(Enemigo([row, col], self.salidas))
                break
            attempts += 1
