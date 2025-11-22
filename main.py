from src.interfaz import MainMenu
import pygame
import sys

# handle main menu logic
#input: none
#output: none

def main():
    while True:
        menu = MainMenu(1200, 800)
        selected = menu.run()
        
        # check user input
        if selected == 'modo_escapa': print(" Modo Escapa")
            
        elif selected == 'modo_cazador': print("Modo Cazador")
            
        elif selected == 'leaderboard': print("Leaderboard")
            
        elif selected == 'dificultad': print("Dificultad")
            
        elif selected in ['salir', 'quit', None]:
            print("eixitng")
            break
            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
