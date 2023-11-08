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
        self.y = display_size[1] / 2
        self.speed = 5
        self.vx = 0
        self.vy = 0
        self.angle = 0

    def draw(self):
        pygame.draw.circle(screen, 'white', (self.x, self.y), self.r)

        end_pos = (self.x + self.r * math.cos(self.angle), self.y + self.r * math.sin(self.angle))
        pygame.draw.line(screen, 'red', (self.x, self.y), end_pos, 3)

    def update(self):
        vx = 0
        vy = 0
        if pressed[pygame.K_d]:
            vx = 1
        elif pressed[pygame.K_a]:
            vx = -1
        else:
            vx = 0
            self.vx = 0
        
        if pressed[pygame.K_w]:
            vy = -1
        elif pressed[pygame.K_s]:
            vy = 1
        else:
            vy = 0
            self.vy = 0

        if vx or vy:
            length = math.sqrt(vx**2 + vy**2)
            self.vx = self.speed * vx / length
            self.vy = self.speed * vy / length

        self.x += self.vx
        self.y += self.vy

        self.angle = math.atan2(mouse.y - self.y, mouse.x - self.x)

        if mouse.click:
            bullets.append(Bullet())

class Circle:
    def __init__(self):
        self.r = random.uniform(20, 50)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
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
        elif self.y + self.r > display_size[1]:
            self.y = display_size[1] - self.r
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
        self.x = player.x + player.r * math.cos(player.angle)
        self.y = player.y + player.r * math.sin(player.angle)
        self.r = 10
        self.speed = 7
        self.vx = self.speed * math.cos(player.angle)
        self.vy = self.speed * math.sin(player.angle)

    def draw(self):
        pygame.draw.circle(screen, 'white', (self.x, self.y), self.r)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        check_x = self.x + self.r < 0 or self.x - self.r > display_size[0]
        check_y = self.y + self.r < 0 or self.y - self.r > display_size[1]
        if check_x or check_y:
            bullets.remove(self)

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.click = False
        self.state = 'up'

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()

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

    pygame.display.flip()