import pygame
import random
import math


class Player:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.w = 40
        self.h = 40
        self.speed = 0.3
        self.vx = 0
        self.vy = 0

    def draw(self, screen):
        pygame.draw.rect(screen, "purple", (self.x, self.y, self.w, self.h))

    def update(self, game):
        self.update_velocity()
        self.move(game.dt)
        self.check_collision(game.walls)

    def update_velocity(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_d]:
            self.vx = self.speed
        elif pressed[pygame.K_a]:
            self.vx = -self.speed
        else:
            self.vx = 0

        if pressed[pygame.K_w]:
            self.vy = -self.speed
        elif pressed[pygame.K_s]:
            self.vy = self.speed
        else:
            self.vy = 0

        if self.vx and self.vy:
            length = math.sqrt(self.vx**2 + self.vy**2)
            self.vx = self.speed * self.vx / length
            self.vy = self.speed * self.vy / length

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_collision(self, walls):
        for wall in walls:
            check_x = self.x + self.w > wall.x and self.x < wall.x + wall.w
            check_y = self.y + self.h > wall.y and self.y < wall.y + wall.h
            if check_x and check_y:
                self.x = 10
                self.y = 10


class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.w, self.h))


class Game1:
    def __init__(self, display_size, screen, clock):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock

        self.running = True
        self.dt = 0
        self.player = Player()
        self.walls = []

        self.create_walls()

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill("black")
        self.dt = self.clock.tick(60)

        self.player.update(self)

        self.player.draw(self.screen)
        for wall in self.walls:
            wall.draw(self.screen)

        pygame.display.flip()

    def create_walls(self):
        for _ in range(10):
            w = random.uniform(50, 100)
            h = random.uniform(50, 100)
            x = random.uniform(100, self.display_size[0] - w)
            y = random.uniform(100, self.display_size[1] - h)
            self.walls.append(Wall(x, y, w, h))