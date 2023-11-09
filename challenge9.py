import pygame


class Player:
    def __init__(self):
        self.w = 50
        self.h = 50
        self.x = boundaries.left + (boundaries.right - boundaries.left) / 2 - self.w / 2
        self.y = boundaries.bottom - self.h
        self.walk_speed = 0.4
        self.jump_speed = 0.8
        self.vx = 0
        self.vy = 0
        self.grounded = True

    def draw(self):
        pygame.draw.rect(screen, "blue", (self.x - game_view.x, self.y - game_view.y, self.w, self.h))

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

        if self.y < boundaries.top:
            self.y = boundaries.top
            self.vy = 0
        elif self.y + self.h > boundaries.bottom:
            self.y = boundaries.bottom - self.h
            self.vy = 0
            self.grounded = True

    def platform_collision(self):
        for platform in platforms:
            check_x = self.x + self.w > platform.x and self.x < platform.x + platform.w
            check_y = self.y + self.h > platform.y and self.y < platform.y + platform.h
            if check_x and check_y:
                prev_x = self.x - self.vx * dt
                prev_y = self.y - self.vy * dt

                def get_time(d, v):
                    time = d / v if v else float("inf")
                    return time if time >= 0 else float("inf")

                time_left = get_time(platform.x - (prev_x + self.w), self.vx)
                time_right = get_time(platform.x + platform.w - prev_x, self.vx)
                time_top = get_time(platform.y - (prev_y + self.h), self.vy)
                time_bottom = get_time(platform.y + platform.h - prev_y, self.vy)

                fastest = min(time_left, time_right, time_top, time_bottom)

                if time_left == fastest:
                    self.x = platform.x - self.w
                    self.vx = 0
                elif time_right == fastest:
                    self.x = platform.x + platform.w
                    self.vx = 0
                elif time_top == fastest:
                    self.y = platform.y - self.h
                    self.vy = 0
                elif time_bottom == fastest:
                    self.y = platform.y + platform.h
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
            pygame.draw.rect(screen, "white", (self.x - game_view.x, self.y - game_view.y, self.w, self.h))


class Boundaries:
    def __init__(self):
        self.left = 0
        self.right = 2000
        self.top = 0
        self.bottom = 1000
        self.size = 100

    def draw(self):
        if game_view.x < self.left:
            pygame.draw.rect(screen, "white", (0, 0, self.left - game_view.x, game_view.h))
        elif game_view.x + game_view.w > self.right:
            pygame.draw.rect(screen, "white", (self.right - game_view.x, 0, game_view.w, game_view.h))

        if game_view.y < self.top:
            pygame.draw.rect(screen, "white", (0, 0, game_view.w, self.top - game_view.y))
        elif game_view.y + game_view.h > self.bottom:
            pygame.draw.rect(screen, "white", (0, self.bottom - game_view.y, game_view.w, game_view.h))


class GameView:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = display_size[0]
        self.h = display_size[1]

    def update(self):
        self.x = player.x + player.w / 2 - self.w / 2
        self.y = player.y + player.h / 2 - self.h / 2

        if self.x < boundaries.left - boundaries.size:
            self.x = boundaries.left - boundaries.size
        elif self.x + self.w > boundaries.right + boundaries.size:
            self.x = boundaries.right - self.w + boundaries.size

        if self.y < boundaries.top - boundaries.size:
            self.y = boundaries.top - boundaries.size
        elif self.y + self.h > boundaries.bottom + boundaries.size:
            self.y = boundaries.bottom - self.h + boundaries.size


class Game9:
    def __init__(self, display_size, screen, clock):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock

        self.running = True
        self.dt = 0


def create_platforms():
    row_num = 8
    column_num = 8
    max_x = 0
    max_y = 0

    for n in range(row_num):
        for m in range(column_num):
            if (n + m) % 2 == 0:
                continue

            x = boundaries.left + (boundaries.right - boundaries.left) / column_num * m
            y = boundaries.top + (boundaries.bottom - boundaries.top) / row_num * n
            platforms.append(Platform(x, y))

            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

    x_offset = (boundaries.right - max_x - platforms[0].w) / 2
    y_offset = (boundaries.bottom - max_y - platforms[0].h) / 2
    for platform in platforms:
        platform.x += x_offset
        platform.y += y_offset


gravity = 0.03
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
