import pygame
import random
import math

pygame.init()
display_size = (1000, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Challenge ")
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = display_size[0] / 2
        self.y = display_size[1] / 2
        self.vx = 0
        self.vy = 0
        self.speed = 0.2
        self.r = 10

    def draw(self):
        pygame.draw.circle(screen, "orange", (self.x, self.y), self.r)

    def update(self):
        self.update_velocity()
        self.move()
        self.check_collision()

    def update_velocity(self):
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

    def move(self):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_collision(self):
        for circle in circles:
            dx = circle.x - self.x
            dy = circle.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist < self.r + circle.r:
                circles.remove(circle)
                self.r += circle.r / 8


class Circle:
    def __init__(self):
        self.r = random.uniform(5, 20)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.click = False
        self.state = "up"

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]

        mouse_down = pygame.mouse.get_pressed()[0]
        if self.state == "up" and mouse_down:
            self.state = "click"
            self.click = True
        elif self.state == "click" and mouse_down:
            self.state = "down"
            self.click = False
        elif not mouse_down:
            self.state = "up"
            self.click = False


def spawn_circles():
    if frame_count % spawn_rate == 0:
        circles.append(Circle())


mouse = Mouse()
player = Player()
circles = []
spawn_rate = 100
frame_count = 0

for _ in range(20):
    circles.append(Circle())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_count += 1
    screen.fill("black")
    dt = clock.tick(60)
    mouse.update()

    spawn_circles()
    for circle in circles:
        circle.draw()

    player.update()
    player.draw()

    pygame.display.flip()
