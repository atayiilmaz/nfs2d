import pygame
from src.game import RacingGame

def main():
    pygame.init()
    pygame.mixer.init()
    game = RacingGame()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()