import pygame
import random
import math


class Player:
    def __init__(self):
        self.r = 30
        self.x = display_size[0] / 2
        self.y = display_size[1] / 2
        self.speed = 0.3
        self.vx = 0
        self.vy = 0
        self.direction = [0, -1]

    def draw(self):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

        end_pos = (self.x + self.r * self.direction[0], self.y + self.r * self.direction[1])
        pygame.draw.line(screen, "red", (self.x, self.y), end_pos, 3)

    def update(self):
        self.update_velocity()
        self.move()
        if mouse.click:
            bullets.append(Bullet())

    def update_velocity(self):
        if len(keyboard.pressed) == 0:
            self.vx = 0
            self.vy = 0
            return
        elif keyboard.pressed[0] == "w":
            self.direction = [0, -1]
        elif keyboard.pressed[0] == "a":
            self.direction = [-1, 0]
        elif keyboard.pressed[0] == "s":
            self.direction = [0, 1]
        elif keyboard.pressed[0] == "d":
            self.direction = [1, 0]

        self.vx = self.direction[0] * self.speed
        self.vy = self.direction[1] * self.speed

    def move(self):
        self.x += self.vx * dt
        self.y += self.vy * dt


class Circle:
    def __init__(self):
        self.r = random.uniform(20, 50)
        self.x = random.uniform(self.r, display_size[0] - self.r)
        self.y = random.uniform(self.r, display_size[1] - self.r)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.vx = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]
        self.vy = random.uniform(0.05, 0.3) * [-1, 1][random.randrange(2)]

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
        self.x = player.x + player.r * player.direction[0]
        self.y = player.y + player.r * player.direction[1]
        self.r = 10
        self.speed = 0.7
        self.vx = self.speed * player.direction[0]
        self.vy = self.speed * player.direction[1]

    def draw(self):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

    def update(self):
        self.x += self.vx * dt
        self.y += self.vy * dt

        check_x = self.x + self.r < 0 or self.x - self.r > display_size[0]
        check_y = self.y + self.r < 0 or self.y - self.r > display_size[1]
        if check_x or check_y:
            bullets.remove(self)


class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.click = False
        self.state = "up"

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()

        down = pygame.mouse.get_pressed()[0]
        if down and self.state == "up":
            self.state = "click"
            self.click = True
        elif down and self.state == "click":
            self.state = "down"
            self.click = False
        elif not down:
            self.state = "up"
            self.click = False


class Keyboard:
    def __init__(self):
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.pressed = []

    def update(self):
        pressed = pygame.key.get_pressed()

        for i in range(4):
            key = ["w", "a", "s", "d"][i]

            if pressed[getattr(pygame, f"K_{key}")]:
                if not getattr(self, key):
                    self.pressed.insert(0, key)
                setattr(self, key, True)
            else:
                if getattr(self, key):
                    self.pressed.remove(key)
                setattr(self, key, False)


class Game6:
    def __init__(self, display_size, screen, clock):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock

        self.running = True
        self.dt = 0


circles = []
bullets = []
player = Player()
mouse = Mouse()
keyboard = Keyboard()

for _ in range(10):
    circles.append(Circle())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    dt = clock.tick(60)

    for circle in circles:
        circle.update()
    for bullet in bullets:
        bullet.update()
    mouse.update()
    keyboard.update()
    player.update()

    for circle in circles:
        circle.draw()
    for bullet in bullets:
        bullet.draw()
    player.draw()

    pygame.display.flip()
