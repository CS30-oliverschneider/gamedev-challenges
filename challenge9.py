import pygame


class Player:
    def __init__(self, boundaries):
        self.w = 50
        self.h = 50
        self.x = boundaries.left + (boundaries.right - boundaries.left) / 2 - self.w / 2
        self.y = boundaries.bottom - self.h
        self.walk_speed = 0.4
        self.jump_speed = 0.8
        self.vx = 0
        self.vy = 0
        self.grounded = True

    def draw(self, game_view, screen):
        pygame.draw.rect(screen, "blue", (self.x - game_view.x, self.y - game_view.y, self.w, self.h))

    def update(self, game):
        self.update_velocity(game.gravity)
        self.move(game.dt)

        self.grounded = False
        self.boundary_collision(game.boundaries)
        self.platform_collision(game.platforms, game.dt)

    def update_velocity(self, gravity):
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

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def boundary_collision(self, boundaries):
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

    def platform_collision(self, platforms, dt):
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
                    self.grounded = True
                elif time_bottom == fastest:
                    self.y = platform.y + platform.h
                    self.vy = 0


class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 150
        self.h = 20

    def draw(self, game_view, screen):
        if self.x + self.w > game_view.x and self.x < game_view.x + game_view.w:
            pygame.draw.rect(screen, "white", (self.x - game_view.x, self.y - game_view.y, self.w, self.h))


class Boundaries:
    def __init__(self):
        self.left = 0
        self.right = 2000
        self.top = 0
        self.bottom = 1000
        self.size = 100

    def draw(self, game_view, screen):
        if game_view.x < self.left:
            pygame.draw.rect(screen, "white", (0, 0, self.left - game_view.x, game_view.h))
        elif game_view.x + game_view.w > self.right:
            pygame.draw.rect(screen, "white", (self.right - game_view.x, 0, game_view.w, game_view.h))

        if game_view.y < self.top:
            pygame.draw.rect(screen, "white", (0, 0, game_view.w, self.top - game_view.y))
        elif game_view.y + game_view.h > self.bottom:
            pygame.draw.rect(screen, "white", (0, self.bottom - game_view.y, game_view.w, game_view.h))


class GameView:
    def __init__(self, display_size):
        self.x = 0
        self.y = 0
        self.w = display_size[0]
        self.h = display_size[1]

    def update(self, player, boundaries):
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

        self.dt = 0
        self.gravity = 0.03
        self.platforms = []
        self.boundaries = Boundaries()
        self.game_view = GameView(self.display_size)
        self.player = Player(self.boundaries)
        self.create_platforms()

    def loop(self):
        self.screen.fill("black")
        self.dt = self.clock.tick(60)

        self.player.update(self)
        self.game_view.update(self.player, self.boundaries)

        for platform in self.platforms:
            platform.draw(self.game_view, self.screen)
        self.boundaries.draw(self.game_view, self.screen)
        self.player.draw(self.game_view, self.screen)

        pygame.display.flip()

    def create_platforms(self):
        row_num = 8
        column_num = 8
        max_x = 0
        max_y = 0

        for n in range(row_num):
            for m in range(column_num):
                if (n + m) % 2 == 0:
                    continue

                x = self.boundaries.left + (self.boundaries.right - self.boundaries.left) / column_num * m
                y = self.boundaries.top + (self.boundaries.bottom - self.boundaries.top) / row_num * n
                self.platforms.append(Platform(x, y))

                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

        x_offset = (self.boundaries.right - max_x - self.platforms[0].w) / 2
        y_offset = (self.boundaries.bottom - max_y - self.platforms[0].h) / 2
        for platform in self.platforms:
            platform.x += x_offset
            platform.y += y_offset
