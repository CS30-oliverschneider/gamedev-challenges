import pygame
import random
import math


class Player:
    def __init__(self, display_size, wall_y):
        self.r = 30
        self.x = display_size[0] / 2
        self.y = wall_y + (display_size[1] - wall_y) / 2
        self.speed = 0.3
        self.vx = 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)
        pygame.draw.line(screen, "red", (self.x, self.y), (self.x, self.y - self.r), 3)

    def update(self, game):
        if game.keyboard.d:
            self.vx = self.speed
        elif game.keyboard.a:
            self.vx = -self.speed
        else:
            self.vx = 0

        self.x += self.vx * game.dt

        if game.mouse.state == "click":
            game.bullets.append(Bullet(self))


class Circle:
    def __init__(self, display_size, wall_y):
        self.r = random.uniform(20, 50)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, wall_y - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.vx = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def update(self, game):
        self.move(game.dt)
        self.wall_collision(game.display_size, game.wall_y)
        self.bullet_collision(game.bullets, game.circles)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def wall_collision(self, display_size, wall_y):
        if self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
        elif self.x + self.r > display_size[0]:
            self.x = display_size[0] - self.r
            self.vx *= -1

        if self.y - self.r < 0:
            self.y = self.r
            self.vy *= -1
        elif self.y + self.r > wall_y:
            self.y = wall_y - self.r
            self.vy *= -1

    def bullet_collision(self, bullets, circles):
        for bullet in bullets:
            dx = bullet.x - self.x
            dy = bullet.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist < self.r + bullet.r:
                circles.remove(self)
                bullets.remove(bullet)


class Bullet:
    def __init__(self, player):
        self.x = player.x
        self.y = player.y - player.r
        self.r = 10
        self.vy = -0.5

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

    def update(self, game):
        self.y += self.vy * game.dt

        if self.y + self.r < 0:
            game.bullets.remove(self)


class Game5:
    def __init__(self, display_size, screen, clock, keyboard, mouse):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock
        self.keyboard = keyboard
        self.mouse = mouse

        self.dt = 0
        self.wall_y = 500
        self.circles = []
        self.bullets = []
        self.player = Player(self.display_size, self.wall_y)

        for _ in range(10):
            self.circles.append(Circle(self.display_size, self.wall_y))

    def loop(self, dt):
        self.screen.fill("black")
        self.dt = dt

        for circle in self.circles:
            circle.update(self)
        for bullet in self.bullets:
            bullet.update(self)
        self.player.update(self)

        for circle in self.circles:
            circle.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)

        pygame.draw.line(self.screen, "white", (0, self.wall_y), (self.display_size[0], self.wall_y), 3)
