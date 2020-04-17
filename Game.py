import pygame, sys, math
from pygame.locals import *
import random

from GameObjects import Asteroid, Player, Shot, get_distance


class Game:
    def __init__(self, window_width: int, window_height: int, lvl: int,
                 asteroids=None):
        self.total_score = 0
        self.p = Player(window_width / 2, window_height / 2, 0, 0, 15,
                        window_width, window_height)
        self.window_width = window_width
        self.window_height = window_height
        self.asteroids = asteroids
        self.lvl = lvl
        self.total_score = 0
        self.win = pygame.display.set_mode((window_width, window_height))
        self.shots = list()
        self.sc = 0

        if not asteroids:
            self.asteroids = list()
            self.add_random_asteroid(lvl + 3)

        pygame.init()
        pygame.font.init()

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
        v = pygame.key.get_pressed()
        if v[pygame.K_LEFT]:
            self.p.turn_at(-0.1)
        if v[pygame.K_RIGHT]:
            self.p.turn_at(0.1)
        if v[pygame.K_SPACE]:
            self.p.add_speed(0.05 * -math.cos(self.p.direction + math.pi),
                             0.05 * - math.sin(self.p.direction + math.pi))
        if v[pygame.K_UP]:
            if self.sc <= 0:
                self.shots.append(
                    Shot(self.p, self.window_width, self.window_height))
                self.sc = 20
        if self.sc > 0:
            self.sc -= 1

    def move_shots(self):
        for i in self.shots:
            i.move()
            i.draw(pygame, self.win)
            i.ticks += 1
            if i.ticks >= 120:
                self.shots.remove(i)

    def move_and_draw_asteroids(self):
        for i in self.asteroids:
            i.move()
            i.draw(pygame, self.win)

    def check_collision(self):
        for j in self.asteroids:
            for i in self.shots:
                if get_distance(j.x, j.y, i.x, i.y) <= j.size:
                    self.shots.remove(i)
                    self.p.score += 1
                    self.asteroids.remove(j)
                    if j.size > 15:
                        self.asteroids.append(
                            Asteroid(j.x, j.y,
                                     j.speed_x + 6 * (random.random() - 0.5),
                                     j.speed_y + 6 * (random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
                        self.asteroids.append(
                            Asteroid(j.x, j.y,
                                     j.speed_x + 6 * (random.random() - 0.5),
                                     j.speed_y + 6 * (random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
                        self.asteroids.append(
                            Asteroid(j.x, j.y,
                                     j.speed_x + 6 * (random.random() - 0.5),
                                     j.speed_y + 6 * (random.random() - 0.5),
                                     10,
                                     self.window_width, self.window_height))
            if get_distance(self.p.x, self.p.y, j.x,
                            j.y) < j.size + self.p.size / 1.5:
                return True
        return False

    def draw_score_and_lvl(self):
        font = pygame.font.Font(None, 32)
        self.win.blit(
            font.render("Score:" + str(self.p.score) + "  Total score:" + str(
                self.total_score) + "  LVL:" + str(self.lvl), 1,
                        (255, 255, 255)),
            (10, 5))

    def start_lvl(self):
        clock = pygame.time.Clock()
        while True:  # основной цикл обработки событий
            clock.tick(60)
            self.win.fill((0, 0, 0))

            self.check_events()
            self.move_shots()
            self.p.move()
            self.p.draw(pygame, self.win)
            self.move_and_draw_asteroids()
            self.draw_score_and_lvl()
            if self.check_collision():
                return False

            pygame.display.update()

            if len(self.asteroids) == 0:
                return True
        return False

    def start(self):
        game_active = True
        while game_active:
            self.__init__(self.window_width, self.window_height, self.lvl + 1)
            game_active = self.start_lvl()
            self.total_score += self.p.score
