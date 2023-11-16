import pygame
import random
import math


class Player:
    def __init__(self, display_size):
        self.x = display_size[0] / 2
        self.y = display_size[1] / 2
        self.vx = 0
        self.vy = 0
        self.speed = 0.2
        self.r = 10

    def draw(self, screen):
        pygame.draw.circle(screen, "orange", (self.x, self.y), self.r)

    def update(self, game):
        self.update_velocity(game.mouse)
        self.move(game.dt)
        self.check_collision(game.circles)

    def update_velocity(self, mouse):
        dx = mouse.x - self.x
        dy = mouse.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist > 5:
            self.vx = dx / dist * self.speed
            self.vy = dy / dist * self.speed
        else:
            self.vx = 0
            self.vy = 0
            self.x = mouse.x
            self.y = mouse.y

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_collision(self, circles):
        for circle in circles:
            dx = circle.x - self.x
            dy = circle.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist < self.r + circle.r:
                circles.remove(circle)
                self.r += circle.r / 8


class Circle:
    def __init__(self, display_size):
        self.r = random.uniform(5, 20)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Game4:
    def __init__(self, display_size, screen, clock, keyboard, mouse):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock
        self.keyboard = keyboard
        self.mouse = mouse

        self.dt = 0
        self.player = Player(self.display_size)
        self.circles = []
        self.spawn_rate = 100
        self.frame_count = 0

        for _ in range(20):
            self.circles.append(Circle(self.display_size))

    def loop(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        self.frame_count += 1
        self.screen.fill("black")
        self.dt = dt

        self.spawn_circles()
        for circle in self.circles:
            circle.draw(self.screen)

        self.player.update(self)
        self.player.draw(self.screen)

    def spawn_circles(self):
        if self.frame_count % self.spawn_rate == 0:
            self.circles.append(Circle(self.display_size))
