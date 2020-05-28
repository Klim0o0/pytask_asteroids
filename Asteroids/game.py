import pygame
import sys
import math
import random
from Asteroids.game_objects import Asteroid, Player, Shot
from Asteroids.menu import Menu
from Asteroids.utils import get_distance


class Game:
    def __init__(self, window_width: int, window_height: int, level: int,
                 asteroids=None):
        self.total_score = 0
        self.player = Player(window_width / 2, window_height / 2, 0, 0, 15,
                             window_width, window_height)
        self.window_width = window_width
        self.window_height = window_height
        self.asteroids = asteroids
        self.level = level
        self.shots = list()
        self.refresh_time = 0
        if not asteroids:
            self.asteroids = list()
            self.add_random_asteroid(level)

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((window_width, window_height))
        self.menu = Menu(pygame, self.window, window_width, window_height)

    def add_random_asteroid(self, asteroids_count: int):
        for i in range(asteroids_count):
            self.asteroids.append(
                Asteroid(int(self.window_width * random.random()),
                         int(self.window_height * random.random()),
                         6 * (random.random() - 0.5),
                         6 * (random.random() - 0.5),
                         12 + int(25 * random.random()), self.window_width,
                         self.window_height))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return True
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_LEFT]:
            self.player.turn_at(-0.1)
        if pressed_key[pygame.K_RIGHT]:
            self.player.turn_at(0.1)
        if pressed_key[pygame.K_SPACE]:
            self.player.add_speed(
                0.05 * -math.cos(self.player.direction + math.pi),
                0.05 * - math.sin(self.player.direction + math.pi))
        if pressed_key[pygame.K_UP]:
            if self.refresh_time <= 0:
                self.shots.append(
                    Shot(self.player, self.window_width, self.window_height))
                self.refresh_time = 20
        if self.refresh_time > 0:
            self.refresh_time -= 1

    def move_shots(self):
        for shot in self.shots:
            shot.move()
            shot.draw(pygame, self.window)
            shot.ticks += 1
            if shot.ticks >= 200:
                self.shots.remove(shot)
            if get_distance(self.player.x, self.player.y, shot.x,
                            shot.y) < self.player.size:
                return True
        return False

    def move_and_draw_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.move()
            asteroid.draw(pygame, self.window)

    def check_collision(self):
        for asteroid in self.asteroids:
            for shot in self.shots:
                if get_distance(asteroid.x, asteroid.y, shot.x,
                                shot.y) <= asteroid.size:
                    self.shots.remove(shot)
                    self.player.score += 1
                    self.total_score += 1
                    self.asteroids.remove(asteroid)
                    if asteroid.size > 15:
                        self.asteroids.append(
                            Asteroid(asteroid.x, asteroid.y,
                                     asteroid.speed_x + 6 * (
                                             random.random() - 0.5),
                                     asteroid.speed_y + 6 * (
                                             random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
                        self.asteroids.append(
                            Asteroid(asteroid.x, asteroid.y,
                                     asteroid.speed_x + 6 * (
                                             random.random() - 0.5),
                                     asteroid.speed_y + 6 * (
                                             random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
                        self.asteroids.append(
                            Asteroid(asteroid.x, asteroid.y,
                                     asteroid.speed_x + 6 * (
                                             random.random() - 0.5),
                                     asteroid.speed_y + 6 * (
                                             random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
            if get_distance(self.player.x, self.player.y, asteroid.x,
                            asteroid.y) < \
                    asteroid.size + self.player.size / 1.5:
                return True
        return False

    def draw_score_and_level_number(self):
        font = pygame.font.Font(None, 32)
        self.window.blit(
            font.render(
                "Score:" + str(self.player.score) + "  Total score:" + str(
                    self.total_score) + "  LVL:" + str(self.level), 1,
                (255, 255, 255)),
            (10, 5))

    def start_level(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 40)
        self.menu.start_menu(font)

        while True:  # основной цикл обработки событий
            clock.tick(60)
            self.window.fill((0, 0, 0))

            if self.check_events():
                self.menu.start_menu(font)
            if self.move_shots():
                self.menu.start_game_over_screen(font)
                self.__init__(self.window_width, self.window_height, 1)

            self.player.move()
            self.player.draw(pygame, self.window)
            self.move_and_draw_asteroids()
            self.draw_score_and_level_number()
            if self.check_collision():
                self.menu.start_game_over_screen(font)
                self.__init__(self.window_width, self.window_height, 1)

            pygame.display.update()
            if len(self.asteroids) == 0:
                self.menu.start_next_lvl_screen(font)
                score = self.total_score
                self.__init__(self.window_width, self.window_height,
                              self.level + 1)
                self.total_score = score

    def start(self):
        self.__init__(self.window_width, self.window_height, 1)
        self.start_level()
