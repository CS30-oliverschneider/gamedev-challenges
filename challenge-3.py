import pygame
import random
 
pygame.init()
display_size = (1000, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Challenge 1')

class Circle:
    def __init__(self):
        self.index = len(shapes) - 1
        self.r = random.uniform(30, 60)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.vx = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]

    def draw(self):
        pygame.draw.circle(screen, 'green', (self.x, self.y), self.r)

    def update(self):
        self.move()
        self.check_collision()

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def check_collision(self):
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

class Rectangle:
    def __init__(self,):
        self.index = len(shapes) - 1
        self.w = random.uniform(50, 100)
        self.h = random.uniform(50, 100)
        self.x = random.uniform(self.w, display_size[0] - self.w)
        self.y = random.uniform(self.h, display_size[0] - self.h)
        self.vx = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]

    def draw(self):
        pygame.draw.rect(screen, 'red', (self.x, self.y, self.w, self.h))

    def update(self):
        self.move()
        self.check_collision()

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def check_collision(self):
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

def create_shapes():
    for _ in range(10):
        shapes.append(Circle())

    for _ in range(10):
        shapes.append(Rectangle())

shapes = []

create_shapes()
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill('black')

    for shape in shapes:
        shape.update()
        shape.draw()

    pygame.display.flip()