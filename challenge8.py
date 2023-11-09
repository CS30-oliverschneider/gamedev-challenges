import pygame


class Player:
    def __init__(self):
        self.w = 50
        self.h = 50
        self.x = game_view.x + game_view.w / 2 - self.w / 2
        self.y = boundaries.bottom - self.h
        self.walk_speed = 0.4
        self.jump_speed = 1
        self.vx = 0
        self.vy = 0
        self.grounded = True

    def draw(self):
        pygame.draw.rect(screen, "blue", (self.x - game_view.x, self.y, self.w, self.h))

    def update(self):
        self.update_velocity()
        self.move()

        self.grounded = False
        self.boundary_collision()
        self.platform_collision()

    def update_velocity(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_d]:
            self.vx = self.walk_speed
        elif pressed[pygame.K_a]:
            self.vx = -self.walk_speed
        else:
            self.vx = 0

        if pressed[pygame.K_w] and self.grounded:
            self.vy = -self.jump_speed
            self.grounded = False

        self.vy += gravity

    def move(self):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def boundary_collision(self):
        if self.x < boundaries.left:
            self.x = boundaries.left
        elif self.x + self.w > boundaries.right:
            self.x = boundaries.right - self.w

        if self.y + self.h > boundaries.bottom:
            self.land(boundaries.bottom)

    def platform_collision(self):
        for platform in platforms:
            check_x = self.x + self.w > platform.x and self.x < platform.x + platform.w
            check_y = self.y + self.h > platform.y and self.y < platform.y + platform.h

            if check_x and check_y:
                self.land(platform.y)

    def land(self, y):
        self.y = y - self.h
        self.vy = 0
        self.grounded = True


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 150
        self.h = 20

    def draw(self):
        if self.x + self.w > game_view.x and self.x < game_view.x + game_view.w:
            pygame.draw.rect(screen, "white", (self.x - game_view.x, self.y, self.w, self.h))


class Boundaries:
    def __init__(self):
        self.left = 0
        self.right = 2000
        self.bottom = 600
        self.width = 100

    def draw(self):
        if game_view.x < self.left:
            pygame.draw.rect(screen, "white", (0, 0, self.left - game_view.x, game_view.h))
        elif game_view.x + game_view.w > self.right:
            pygame.draw.rect(screen, "white", (self.right - game_view.x, 0, game_view.w, game_view.h))

        pygame.draw.rect(screen, "white", (0, self.bottom, game_view.w, self.bottom))


class GameView:
    def __init__(self):
        self.w = display_size[0]
        self.h = display_size[1]
        self.x = boundaries.left + (boundaries.right - boundaries.left) / 2 - self.w / 2

    def update(self):
        self.x = player.x + player.w / 2 - self.w / 2

        if self.x < boundaries.left - boundaries.width:
            self.x = boundaries.left - boundaries.width
        elif self.x + self.w > boundaries.right + boundaries.width:
            self.x = boundaries.right - self.w + boundaries.width


class Game8:
    def __init__(self, display_size, screen, clock):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock

        self.running = True
        self.dt = 0


def create_platforms():
    platform_num = 10
    for n in range(platform_num):
        x = (boundaries.right - boundaries.left) / platform_num * n
        y = 475 if n % 2 == 0 else 350
        platforms.append(Platform(x, y))

        if n == platform_num - 1:
            max_x = x + platforms[0].w

    offset = (boundaries.right - boundaries.left - max_x) / 2
    for platform in platforms:
        platform.x += offset


gravity = 0.05
platforms = []
boundaries = Boundaries()
game_view = GameView()
player = Player()
create_platforms()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill("black")
    dt = clock.tick(60)

    player.update()
    game_view.update()

    for platform in platforms:
        platform.draw()
    boundaries.draw()
    player.draw()

    pygame.display.flip()
