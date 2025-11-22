import pygame
import sys


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
    

'''
class GameWindow():
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Modo x")
        self.clock = pygame.time.Clock()
'''
        