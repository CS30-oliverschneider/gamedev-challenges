import pygame
import random
import math
 
pygame.init()
display_size = (1000, 700)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Challenge 5')
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.r = 30
        self.x = display_size[0] / 2
        self.y = wall_y + (display_size[1] - wall_y) / 2
        self.speed = 5
        self.vx = 0

    def draw(self):
        pygame.draw.circle(screen, 'white', (self.x, self.y), self.r)
        pygame.draw.line(screen, 'red', (self.x, self.y), (self.x, self.y - self.r), 3)

    def update(self):
        if pressed[pygame.K_d]:
            self.vx = self.speed
        elif pressed[pygame.K_a]:
            self.vx = -self.speed
        else:
            self.vx = 0

        self.x += self.vx

        if mouse.click:
            bullets.append(Bullet())

class Circle:
    def __init__(self):
        self.r = random.uniform(20, 50)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, wall_y - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.vx = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1,1][random.randrange(2)]

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def update(self):
        self.move()
        self.wall_collision()
        self.bullet_collision()

    def move(self):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def wall_collision(self):
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

    def bullet_collision(self):
        for bullet in bullets:
            dx = bullet.x - self.x
            dy = bullet.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist < self.r + bullet.r:
                circles.remove(self)
                bullets.remove(bullet)

class Bullet:
    def __init__(self):
        self.x = player.x
        self.y = player.y - player.r
        self.r = 10
        self.vy = -5

    def draw(self):
        pygame.draw.circle(screen, 'white', (self.x, self.y), self.r)

    def update(self):
        self.y += self.vy

        if self.y + self.r < 0:
            bullets.remove(self)

class Mouse:
    def __init__(self):
        self.click = False
        self.state = 'up'

    def update(self):
        down = pygame.mouse.get_pressed()[0]
        if down and self.state == 'up':
            self.state = 'click'
            self.click = True
        elif down and self.state == 'click':
            self.state = 'down'
            self.click = False
        elif not down:
            self.state = 'up'
            self.click = False

wall_y = 500
circles = []
bullets = []
player = Player()
mouse = Mouse()

for _ in range(10):
    circles.append(Circle())
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill('black')
    dt = clock.tick(60)

    for circle in circles:
        circle.update()
    for bullet in bullets:
        bullet.update()
    mouse.update()
    player.update()

    for circle in circles:
        circle.draw()
    for bullet in bullets:
        bullet.draw()
    player.draw()

    pygame.draw.line(screen, 'white', (0, wall_y), (display_size[0], wall_y), 3)

    pygame.display.flip()