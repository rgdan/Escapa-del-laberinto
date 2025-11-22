from src.interfaz import  MainMenu , GameWindow
from src.mapa import GeneradorMapa
import pygame
import sys


# handle main menu logic
#input: none
#output: none

def main():
    while True:
        menu = MainMenu(1200, 800)
        selected = menu.run()
        

        generador = GeneradorMapa()
        mapa = generador.generar()
        
        #TODO: dibujar cuadriculas del mapa, por ahora solo se imprime la matriz

        # check user input
        if selected == 'modo_escapa': 
            print("Modo Escapa ")
            game = GameWindow(mapa, title="Modo Escapa", width=1200, height=800, cell_size=24)
            game.loop()

        elif selected == 'modo_cazador':
            print("Modo Cazador")
            game = GameWindow(mapa, title="Modo Cazador", width=1200, height=800, cell_size=24)
            game.loop()

            
        elif selected == 'leaderboard': print("Leaderboard")
            
        elif selected == 'dificultad': print("Dificultad")
            
        elif selected in ['salir', 'quit', None]:
            print("eixitng")
            break
            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
