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
        self.game = games[self.index](display_size, screen, clock, keyboard, mouse)
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

    def check_select(self):
        check_x = mouse.x > self.x and mouse.x < self.x + self.w
        check_y = mouse.y > self.y and mouse.y < self.y + self.h
        if check_x and check_y:
            global selected
            selected = self.index

            if mouse.state == "click":
                run_level(self.index)


class Keyboard:
    def __init__(self):
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.escape = False
        self.left = "up"
        self.right = "up"

        self.history = []
        self.pressed = None

    def update(self):
        self.pressed = pygame.key.get_pressed()

        self.w = self.set_bool("w")
        self.a = self.set_bool("a")
        self.s = self.set_bool("s")
        self.d = self.set_bool("d")
        self.escape = self.set_bool("ESCAPE")

        self.left = self.set_state(self.left, "LEFT")
        self.right = self.set_state(self.right, "RIGHT")

    def set_state(self, current_state, key_name):
        key_down = self.pressed[getattr(pygame, f"K_{key_name}")]

        if key_down and current_state == "up":
            return "press"
        elif key_down and current_state == "press":
            return "down"
        elif not key_down:
            return "up"

    def set_bool(self, key_name):
        key_down = self.pressed[getattr(pygame, f"K_{key_name}")]

        if key_down and key_name not in self.history:
            self.history.insert(0, key_name)
        elif not key_down and key_name in self.history:
            self.history.remove(key_name)

        return key_down


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "up"

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        down = pygame.mouse.get_pressed()[0]

        if self.state == "up" and down:
            self.state = "click"
        elif self.state == "click" and down:
            self.state = "down"
        elif not down:
            self.state = "up"


games = [Game1, Game2, Game3, Game4, Game5, Game6, Game7, Game8, Game9]
levels = []
mouse = Mouse()
keyboard = Keyboard()
font = pygame.font.Font("freesansbold.ttf", 70)
selected = 0

for i in range(len(games)):
    levels.append(Level())


def run_level(level_num):
    game_state = "running"
    while game_state == "running":
        level = levels[level_num]
        dt = clock.tick(60)
        keyboard.update()
        mouse.update()
        level.game.loop(dt)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"

        if keyboard.escape:
            game_state = "menu"
        elif keyboard.left == "press":
            level_num = (level_num + 17) % 9
        elif keyboard.right == "press":
            level_num = (level_num + 1) % 9

    if game_state == "quit":
        exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0, 20, 40))
    clock.tick(60)
    selected = None
    mouse.update()

    for level in levels:
        level.check_select()
        level.draw()

    pygame.display.flip()
