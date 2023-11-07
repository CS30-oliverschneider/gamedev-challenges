import pygame
import random
 
pygame.init()
display_size = (1000, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Challenge 2')

class Player:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.w = 40
        self.h = 40
        self.speed = 0.3
        self.vx = 0
        self.vy = 0

    def draw(self):
        pygame.draw.rect(screen, 'purple', (self.x, self.y, self.w, self.h))

    def update(self):
        self.move()
        self.check_collision()

    def move(self):
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

        self.x += self.vx
        self.y += self.vy
    
    def check_collision(self):
        for wall in walls:
            check_x = self.x + self.w > wall.x and self.x < wall.x + wall.w
            check_y = self.y + self.h > wall.y and self.y < wall.y + wall.h
            if check_x and check_y:
                prev_x = self.x - self.vx
                prev_y = self.y - self.vy

                def get_time(d, v):
                    time = d / v if v else float('inf')
                    return time if time >= 0 else float('inf')

                time_left = get_time(wall.x - (prev_x + self.w), self.vx)
                time_right = get_time(wall.x + wall.w - prev_x, self.vx)
                time_top = get_time(wall.y - (prev_y + self.h), self.vy)
                time_bottom = get_time(wall.y + wall.h - prev_y, self.vy)
                
                fastest = min(time_left, time_right, time_top, time_bottom)

                if time_left == fastest:
                    self.x = wall.x - self.w
                elif time_right == fastest:
                    self.x = wall.x + wall.w
                elif time_top == fastest:
                    self.y = wall.y - self.h
                elif time_bottom == fastest:
                    self.y = wall.y + wall.h

class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pygame.draw.rect(screen, 'white', (self.x, self.y, self.w, self.h))

def create_walls():
    for _ in range(10):
        w = random.uniform(50, 100)
        h = random.uniform(50, 100)
        x = random.uniform(100, display_size[0] - w)
        y = random.uniform(100, display_size[1] - h)
        walls.append(Wall(x, y, w, h))

player = Player()
walls = []
create_walls()
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill('black')
    player.update()
    player.draw()
    for wall in walls:
        wall.draw()

    pygame.display.flip()