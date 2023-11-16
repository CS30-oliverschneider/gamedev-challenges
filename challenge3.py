import pygame
import random
import math


class Circle:
    def __init__(self, display_size):
        self.r = random.uniform(30, 60)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.vx = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]

    def draw(self, screen):
        pygame.draw.circle(screen, "green", (self.x, self.y), self.r)

    def update(self, game):
        self.move(game.dt)
        self.wall_collision(game.display_size)
        self.mouse_collision(game.mouse, game.circles, game.win)

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

    def mouse_collision(self, mouse, circles, win):
        if not mouse.state == "click":
            return

        dx = mouse.x - self.x
        dy = mouse.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.r:
            circles.remove(self)
            if len(circles) == 0:
                win()


class Rectangle:
    def __init__(self, display_size):
        self.w = random.uniform(50, 100)
        self.h = random.uniform(50, 100)
        self.x = random.uniform(self.w, display_size[0] - self.w)
        self.y = random.uniform(self.h, display_size[0] - self.h)
        self.vx = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]

    def draw(self, screen):
        pygame.draw.rect(screen, "red", (self.x, self.y, self.w, self.h))

    def update(self, game):
        self.move(game.dt)
        self.wall_collision(game.display_size)
        self.mouse_collision(game.mouse, game.lose)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def wall_collision(self, display_size):
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        elif self.x + self.w > display_size[0]:
            self.x = display_size[0] - self.w
            self.vx *= -1

        if self.y < 0:
            self.y = 0
            self.vy *= -1
        elif self.y + self.h > display_size[1]:
            self.y = display_size[1] - self.h
            self.vy *= -1

    def mouse_collision(self, mouse, lose):
        if not mouse.state == "click":
            return

        check_x = mouse.x > self.x and mouse.x < self.x + self.w
        check_y = mouse.y > self.y and mouse.y < self.y + self.h

        if check_x and check_y:
            lose()


class Game3:
    def __init__(self, display_size, screen, clock, keyboard, mouse):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock
        self.keyboard = keyboard
        self.mouse = mouse

        self.dt = 0
        self.circles = []
        self.rectangles = []

        self.create_shapes()

    def loop(self, dt):
        self.screen.fill("black")
        self.dt = dt

        for circle in self.circles:
            circle.update(self)
        for rectangle in self.rectangles:
            rectangle.update(self)

        for circle in self.circles:
            circle.draw(self.screen)
        for rectangle in self.rectangles:
            rectangle.draw(self.screen)

    def win(self):
        print("Game Over - You WIN!")
        self.create_shapes()

    def lose(self):
        print("Game Over - You LOSE!")
        self.create_shapes()

    def create_shapes(self):
        self.circles.clear()
        self.rectangles.clear()

        for _ in range(10):
            self.circles.append(Circle(self.display_size))

        for _ in range(10):
            self.rectangles.append(Rectangle(self.display_size))
