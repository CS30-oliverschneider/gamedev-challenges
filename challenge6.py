import pygame
import random
import math


class Player:
    def __init__(self, display_size):
        self.r = 30
        self.x = display_size[0] / 2
        self.y = display_size[1] / 2
        self.speed = 0.3
        self.vx = 0
        self.vy = 0
        self.direction = [0, -1]

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

        end_pos = (self.x + self.r * self.direction[0], self.y + self.r * self.direction[1])
        pygame.draw.line(screen, "red", (self.x, self.y), end_pos, 3)

    def update(self, game):
        self.update_velocity(game.keyboard)
        self.move(game.dt)
        if game.mouse.state == "click":
            game.bullets.append(Bullet(self))

    def update_velocity(self, keyboard):
        if len(keyboard.history) == 0:
            self.vx = 0
            self.vy = 0
            return
        elif keyboard.history[0] == "w":
            self.direction = [0, -1]
        elif keyboard.history[0] == "a":
            self.direction = [-1, 0]
        elif keyboard.history[0] == "s":
            self.direction = [0, 1]
        elif keyboard.history[0] == "d":
            self.direction = [1, 0]

        self.vx = self.direction[0] * self.speed
        self.vy = self.direction[1] * self.speed

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


class Circle:
    def __init__(self, display_size):
        self.r = random.uniform(20, 50)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.vx = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def update(self, game):
        self.move(game.dt)
        self.wall_collision(game.display_size)
        self.bullet_collision(game.bullets, game.circles)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def wall_collision(self, display_size):
        if self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
        elif self.x + self.r > display_size[0]:
            self.x = display_size[0] - self.r
            self.vx *= -1

        if self.y - self.r < 0:
            self.y = self.r
            self.vy *= -1
        elif self.y + self.r > display_size[1]:
            self.y = display_size[1] - self.r
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
        self.x = player.x + player.r * player.direction[0]
        self.y = player.y + player.r * player.direction[1]
        self.r = 10
        self.speed = 0.7
        self.vx = self.speed * player.direction[0]
        self.vy = self.speed * player.direction[1]

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

    def update(self, game):
        self.x += self.vx * game.dt
        self.y += self.vy * game.dt

        check_x = self.x + self.r < 0 or self.x - self.r > game.display_size[0]
        check_y = self.y + self.r < 0 or self.y - self.r > game.display_size[1]
        if check_x or check_y:
            game.bullets.remove(self)


class Game6:
    def __init__(self, display_size, screen, clock, keyboard, mouse):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock
        self.keyboard = keyboard
        self.mouse = mouse

        self.dt = 0
        self.circles = []
        self.bullets = []
        self.player = Player(self.display_size)

        for _ in range(10):
            self.circles.append(Circle(self.display_size))

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
