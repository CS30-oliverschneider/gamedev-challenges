import pygame
 
pygame.init()
display_size = (1000, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Challenge ')
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill('black')

    pygame.display.flip()