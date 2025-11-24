from src.interfaz import MainMenu, GameWindow, PlayerRegistration, Leaderboard, HowToPlay
from src.mapa import GeneradorMapa
from src.puntuacion import ScoreManager
import pygame
import sys

# handle main menu logic
#input: none
#output: none

def main():
    # Inicializar el gestor de puntuaciones
    score_manager = ScoreManager()
    current_player = None
    
    while True:
        menu = MainMenu(1200, 800)
        selected = menu.run()
        
        # check user input
        if selected == 'modo_escapa' or selected == 'modo_cazador':
            # Registro obligatorio antes de comenzar
            registration = PlayerRegistration(1200, 800)
            current_player = registration.run()
            
            if not current_player: continue
            
            generador = GeneradorMapa()
            mapa, inicio, salidas = generador.generar()
            
            if selected == 'modo_escapa':
                title = "Modo Escapa"
                print(f"Modo Escapa - Jugador: {current_player}")
            else:
                title = "Modo Cazador"
                print(f"Modo Cazador - Jugador: {current_player}")
            
            game = GameWindow(mapa, title, 1200, 800, 48, current_player, inicio, selected, salidas)
            game.loop()
            
            # Después de que termine el juego (dentro del loop principal):
            if game.game_won:
                final_score = game.get_final_score()
                player_name = game.get_player_name()
                
                if final_score is not None:
                    # Determinar el modo para guardar el score
                    modo = 'escapa' if game.modo == 'modo_escapa' else 'cazador'
                    
                    # Agregar el score
                    is_top_5 = score_manager.add_score(player_name, final_score, modo)
                    
                    if is_top_5:
                        rank = score_manager.get_rank(player_name, final_score, modo)
                        print(f"¡Nuevo récord! Posición #{rank} en el Top 5")

        elif selected == 'leaderboard':
            leaderboard = Leaderboard(1200, 800, score_manager)
            leaderboard.run()
        
        elif selected == 'como_jugar':
            how_to_play = HowToPlay(1200, 800)
            how_to_play.run()
            
        elif selected == 'dificultad': print("Dificultad")
            
        elif selected in ['salir', 'quit', None]:
            print("Exiting game...")
            break
            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
