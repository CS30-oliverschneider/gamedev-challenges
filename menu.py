import pygame

from challenge1 import Game1
from challenge2 import Game2
from challenge3 import Game3
from challenge4 import Game4

# from challenge5 import Game5
# from challenge6 import Game6
# from challenge7 import Game7
# from challenge8 import Game8
# from challenge9 import Game9

pygame.init()
display_size = (1000, 600)
screen = pygame.display.set_mode(display_size)
clock = pygame.time.Clock()

game = Game2(display_size, screen, clock)

while game.running:
    game.loop()
