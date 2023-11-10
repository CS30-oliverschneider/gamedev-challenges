import pygame

from challenge1 import Game1
from challenge2 import Game2
from challenge3 import Game3
from challenge4 import Game4
from challenge5 import Game5
from challenge6 import Game6
from challenge7 import Game7
from challenge8 import Game8
from challenge9 import Game9

pygame.init()
display_size = (1000, 700)
screen = pygame.display.set_mode(display_size)
clock = pygame.time.Clock()


class Level:
    def __init__(self):
        self.index = len(levels)
        self.game = games[self.index](display_size, screen, clock)
        self.w = 150
        self.h = 150

        max_x = 2 * display_size[0] / 3 + self.w
        max_y = 2 * display_size[1] / 3 + self.h
        self.x = self.index % 3 * display_size[0] / 3 + (display_size[0] - max_x) / 2
        self.y = self.index // 3 * display_size[1] / 3 + (display_size[1] - max_y) / 2

        self.text = font.render(str(self.index + 1), True, "#9BBEC8")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.x + self.w / 2, self.y + self.h / 2

    def draw(self):
        pygame.draw.rect(screen, "#164863", (self.x, self.y, self.w, self.h))
        screen.blit(self.text, self.text_rect)
        if selected == self.index:
            pygame.draw.rect(screen, "#DDF2FD", (self.x, self.y, self.w, self.h), 3)


class Keyboard:
    def __init__(self):
        self.left = "up"
        self.right = "up"
        self.up = "up"
        self.down = "up"

        self.w = "up"
        self.a = "up"
        self.s = "up"
        self.d = "up"

        self.enter = False
        self.escape = False

    def update(self):
        pressed = pygame.key.get_pressed()

        key_list = ["LEFT", "RIGHT", "UP", "DOWN", "w", "a", "s", "d"]
        for i in range(len(key_list)):
            key_name = key_list[i]
            key_property = key_name.lower()
            key_down = pressed[getattr(pygame, f"K_{key_name}")]
            key_state = getattr(self, key_property)

            if key_down and key_state == "up":
                setattr(self, key_property, "press")
            elif key_down and key_state == "press":
                setattr(self, key_property, "down")
            elif not key_down:
                setattr(self, key_property, "up")

        if pressed[pygame.K_RETURN]:
            self.enter = True
        else:
            self.enter = False

        if pressed[pygame.K_ESCAPE]:
            self.escape = True
        else:
            self.escape = False


games = [Game1, Game2, Game3, Game4, Game5, Game6, Game7, Game8, Game9]
levels = []
keyboard = Keyboard()
font = pygame.font.Font("freesansbold.ttf", 70)
selected = 0

for i in range(len(games)):
    levels.append(Level())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 20, 40))
    clock.tick(60)
    keyboard.update()

    if keyboard.up == "press" or keyboard.w == "press":
        selected = (selected + 6) % 9
    elif keyboard.left == "press" or keyboard.a == "press":
        selected = (selected + 2) % 3 + selected // 3 * 3
    elif keyboard.down == "press" or keyboard.s == "press":
        selected = (selected + 3) % 9
    elif keyboard.right == "press" or keyboard.d == "press":
        selected = (selected + 1) % 3 + selected // 3 * 3

    for level in levels:
        level.draw()

    if keyboard.enter:
        game_state = "running"
        while game_state == "running":
            level = levels[selected]
            level.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = "quit"

            keyboard.update()
            if keyboard.escape:
                game_state = "menu"
            elif keyboard.left == "press":
                selected = (selected + 17) % 9
            elif keyboard.right == "press":
                selected = (selected + 1) % 9

        if game_state == "quit":
            running = False

    pygame.display.flip()
