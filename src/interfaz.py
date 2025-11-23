import pygame
import sys

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
        button_height = int(height * 0.1) 
        button_x = (width - button_width) // 2
        start_y = int(height * 0.333)
        spacing = int(height * 0.133)
        
        # list of buttons to create
        self.buttons = [
            Button(button_x, start_y, button_width, button_height, "Modo Escapa", "modo_escapa", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing, button_width, button_height, "Modo Cazador", "modo_cazador", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 2, button_width, button_height, "Leaderboard", "leaderboard", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 3, button_width, button_height, "Dificultad", "dificultad", self.BUTTON_COLOR),
            Button(button_x, start_y + spacing * 4, button_width, button_height, "Salir", "salir", self.BUTTON_EXIT_COLOR)
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

# class for the game window

class GameWindow:
    def __init__(self, mapa, title, width, height, cell_size):
        """
        mapa: lista de listas (matriz) con símbolos como '.' y '#'
        cell_size: tamaño de cada celda en píxeles
        """
        pygame.init()
        self.mapa = mapa
        self.title = title
        self.rows = len(mapa)
        self.cols = len(mapa[0]) 

        self.width = width
        self.height = height
        self.cell_size = cell_size
        

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

        # Cargar texturas
        self.texture_camino = pygame.image.load("sprites/background/camino.png")
        self.texture_muro = pygame.image.load("sprites/background/muro.png")
        self.texture_tunel = pygame.image.load("sprites/background/tunel.png")
        self.texture_lianas = pygame.image.load("sprites/background/lianas.png")
        
        # Escalar texturas al tamaño de celda
        self.texture_camino = pygame.transform.scale(self.texture_camino, (self.cell_size, self.cell_size))
        self.texture_muro = pygame.transform.scale(self.texture_muro, (self.cell_size, self.cell_size))
        self.texture_tunel = pygame.transform.scale(self.texture_tunel, (self.cell_size, self.cell_size))
        self.texture_lianas = pygame.transform.scale(self.texture_lianas, (self.cell_size, self.cell_size))

        # Paleta (backup colors)
        self.color_bg = (34, 139, 34)      # verde
        self.color_grid = (0, 0, 0)        #negro

        # Calcular área de dibujo y centrar
        self.grid_w = self.cols * (self.cell_size ) 
        self.grid_h = self.rows * (self.cell_size ) 
        self.offset_y = max(0, (self.height - self.grid_h) // 2)
        self.offset_x = max(0, (self.width - self.grid_w) // 2)

    def draw_grid(self):
        self.screen.fill(self.color_bg)
        for x in range(self.rows):
            for y in range(self.cols):
                celda = self.mapa[x][y]
                pos_x = self.offset_x + y * self.cell_size
                pos_y = self.offset_y + x * self.cell_size
                
                if celda == 0:
                    texture = self.texture_camino
                elif celda == 1:
                    texture = self.texture_muro
                elif celda == 2:
                    texture = self.texture_lianas
                elif celda == 3:
                    texture = self.texture_tunel
                
                self.screen.blit(texture, (pos_x, pos_y))
                
                # Draw grid border
                rect = pygame.Rect(pos_x, pos_y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.color_grid, rect, 1)
        pygame.display.flip()

    # run game untill window is closed or ESC is pressed
    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.running = False

            self.draw_grid()
