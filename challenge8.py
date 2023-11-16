import pygame


class Player:
    def __init__(self, game_view, boundaries):
        self.w = 50
        self.h = 50
        self.x = game_view.x + game_view.w / 2 - self.w / 2
        self.y = boundaries.bottom - self.h
        self.walk_speed = 0.4
        self.jump_speed = 1
        self.vx = 0
        self.vy = 0
        self.grounded = True

    def draw(self, game_view, screen):
        pygame.draw.rect(screen, "blue", (self.x - game_view.x, self.y, self.w, self.h))

    def update(self, game):
        self.update_velocity(game.gravity, game.keyboard)
        self.move(game.dt)

        self.grounded = False
        self.boundary_collision(game.boundaries)
        self.platform_collision(game.platforms)

    def update_velocity(self, gravity, keyboard):
        if keyboard.d:
            self.vx = self.walk_speed
        elif keyboard.a:
            self.vx = -self.walk_speed
        else:
            self.vx = 0

        if keyboard.w and self.grounded:
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

        if self.y + self.h > boundaries.bottom:
            self.land(boundaries.bottom)

    def platform_collision(self, platforms):
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

    def draw(self, game_view, screen):
        if self.x + self.w > game_view.x and self.x < game_view.x + game_view.w:
            pygame.draw.rect(screen, "white", (self.x - game_view.x, self.y, self.w, self.h))


class Boundaries:
    def __init__(self):
        self.left = 0
        self.right = 2000
        self.bottom = 600
        self.width = 100

    def draw(self, game_view, screen):
        if game_view.x < self.left:
            pygame.draw.rect(screen, "white", (0, 0, self.left - game_view.x, game_view.h))
        elif game_view.x + game_view.w > self.right:
            pygame.draw.rect(screen, "white", (self.right - game_view.x, 0, game_view.w, game_view.h))

        pygame.draw.rect(screen, "white", (0, self.bottom, game_view.w, self.bottom))


class GameView:
    def __init__(self, display_size, boundaries):
        self.w = display_size[0]
        self.h = display_size[1]
        self.x = boundaries.left + (boundaries.right - boundaries.left) / 2 - self.w / 2

    def update(self, game):
        self.x = game.player.x + game.player.w / 2 - self.w / 2

        if self.x < game.boundaries.left - game.boundaries.width:
            self.x = game.boundaries.left - game.boundaries.width
        elif self.x + self.w > game.boundaries.right + game.boundaries.width:
            self.x = game.boundaries.right - self.w + game.boundaries.width


class Game8:
    def __init__(self, display_size, screen, clock, keyboard, mouse):
        self.display_size = display_size
        self.screen = screen
        self.clock = clock
        self.keyboard = keyboard
        self.mouse = mouse

        self.dt = 0
        self.gravity = 0.05
        self.platforms = []
        self.boundaries = Boundaries()
        self.game_view = GameView(self.display_size, self.boundaries)
        self.player = Player(self.game_view, self.boundaries)
        self.create_platforms()

    def loop(self, dt):
        self.screen.fill("black")
        self.dt = dt

        self.player.update(self)
        self.game_view.update(self)

        for platform in self.platforms:
            platform.draw(self.game_view, self.screen)
        self.boundaries.draw(self.game_view, self.screen)
        self.player.draw(self.game_view, self.screen)

    def create_platforms(self):
        platform_num = 10
        for n in range(platform_num):
            x = (self.boundaries.right - self.boundaries.left) / platform_num * n
            y = 475 if n % 2 == 0 else 350
            self.platforms.append(Platform(x, y))

            if n == platform_num - 1:
                max_x = x + self.platforms[0].w

        offset = (self.boundaries.right - self.boundaries.left - max_x) / 2
        for platform in self.platforms:
            platform.x += offset
