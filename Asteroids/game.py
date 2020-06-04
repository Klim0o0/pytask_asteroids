import pygame
import sys
import math
import random
from Asteroids.game_objects import Asteroid, Player, Shot, HpBonus, \
    ShieldBonus, RateOfFireBonus, UFO
from Asteroids.menu import Menu
from Asteroids.utils import get_distance


class Game:
    def __init__(self, resolution, level: int, difficult: int, scoreboard,
                 name, asteroids=None):
        self.total_score = 0
        self.player = Player(resolution[0] / 2, resolution[1] / 2, 0, 0, 15,
                             resolution[0], resolution[1])
        self.window_width = resolution[0]
        self.window_height = resolution[1]
        self.asteroids = asteroids
        self.level = level
        self.shots = list()
        self.hp_bonuses = list()
        self.shield_bonuses = list()
        self.rate_fire_bonuses = list()
        self.u_f_o_list = list()
        self.refresh_time = 0
        self.refresh_speed = 1
        self.difficult = difficult
        self.scoreboard = scoreboard
        self.name = name
        if not asteroids:
            self.asteroids = list()
            self.add_random_asteroid(level * difficult)

        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        self.menu = Menu(pygame, self.window, self.window_width,
                         self.window_height)
        self.default_immortal_time = 100 / difficult

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
            self.refresh_time -= self.refresh_speed

    def move_shots(self):
        for shot in self.shots:
            shot.move()
            shot.draw(pygame, self.window)
            shot.ticks += 1
            if shot.ticks >= 200:
                self.shots.remove(shot)
            if get_distance(self.player.x, self.player.y, shot.x,
                            shot.y) < self.player.size:
                self.shots.remove(shot)
                if self.player.immortal_time <= 0:
                    self.player.immortal_time = self.default_immortal_time
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

                    if random.random() < 0.3:
                        self.create_bonus(asteroid)

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
                if self.player.immortal_time <= 0:
                    self.player.immortal_time = self.default_immortal_time
                    return True
        return False

    def draw_score_and_level_number(self):
        font = pygame.font.Font(None, 32)
        self.window.blit(
            font.render(
                "Score:" + str(self.player.score) + "  Total score:" + str(
                    self.total_score) + "  LVL:" + str(
                    self.level) + "  HP:" + str(self.player.health), 1,
                (255, 255, 255)),
            (10, 5))

    def start_level(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 40)
        self.menu.start_menu(font)
        self.player.immortal_time = self.default_immortal_time

        while True:  # основной цикл обработки событий
            clock.tick(60)
            self.window.fill((0, 0, 0))
            if self.player.immortal_time > 0:
                self.player.immortal_time -= 1

            if self.check_events():
                self.menu.start_menu(font)
            if self.move_shots():
                self.game_over()

            self.check_bonuses_collision()
            self.draw_bonuses()

            self.player.move()
            self.player.draw(pygame, self.window)

            self.u_f_o_iteration()

            self.move_and_draw_asteroids()

            self.draw_score_and_level_number()

            if self.check_collision() or self.check_u_f_o_player_collision():
                self.game_over()

            if len(self.asteroids) == 0:
                self.menu.start_next_lvl_screen(font)
                score = self.total_score
                health = self.player.health
                self.__init__((self.window_width, self.window_height),
                              self.level + 1, self.difficult, self.scoreboard,
                              self.name)
                self.total_score = score
                self.player.health = health

            pygame.display.update()

    def change_scoreboard(self,f:str):
        h = 0
        l = list()
        for i in range(len(self.scoreboard)):
            if i == 5:
                break
            if self.scoreboard[i][1] < self.total_score and h == 0:
                l.append((self.name, self.total_score))
                h = 1
            else:
                l.append(self.scoreboard[i - +h])
        self.scoreboard = l

        s = ""
        for i in self.scoreboard:
            s += i[0] + ' ' + str(i[1]) + '\n'

        with open(f, 'w') as file:
            file.write(s)

    def game_over(self):
        self.player.health -= 1
        if self.player.health == 0:
            self.change_scoreboard('scoreboard.txt')
            self.menu.start_game_over_screen(pygame.font.Font(None, 40),
                                             self.scoreboard)
            self.__init__((self.window_width, self.window_height), 1,
                          self.difficult, self.scoreboard, self.name)
        else:
            self.set_player_default_position()

    def create_bonus(self, game_object):
        r = random.randint(1, 3)
        if r == 1:
            self.hp_bonuses.append(
                HpBonus(game_object, self.window_width, self.window_height))
        if r == 2:
            self.shield_bonuses.append(
                ShieldBonus(game_object, self.window_width,
                            self.window_height))
        if r == 3:
            self.rate_fire_bonuses.append(
                RateOfFireBonus(game_object, self.window_width,
                                self.window_height))

    def draw_bonuses(self):
        for hp_bonus in self.hp_bonuses:
            hp_bonus.draw(pygame, self.window)
        for shield_bonus in self.shield_bonuses:
            shield_bonus.draw(pygame, self.window)
        for rate_fire_bonus in self.rate_fire_bonuses:
            rate_fire_bonus.draw(pygame, self.window)

    def check_bonuses_collision(self):
        for hp_bonus in self.hp_bonuses:
            if get_distance(self.player.x, self.player.y, hp_bonus.x,
                            hp_bonus.y) < self.player.size + hp_bonus.size:
                self.hp_bonuses.remove(hp_bonus)
                self.player.health += 1
        for shield_bonus in self.shield_bonuses:
            if get_distance(self.player.x, self.player.y, shield_bonus.x,
                            shield_bonus.y) < self.player.size \
                    + shield_bonus.size:
                self.shield_bonuses.remove(shield_bonus)
                self.player.immortal_time = self.default_immortal_time * 2
        for rate_fire_bonus in self.rate_fire_bonuses:
            if get_distance(self.player.x, self.player.y, rate_fire_bonus.x,
                            rate_fire_bonus.y) \
                    < self.player.size + rate_fire_bonus.size:
                self.rate_fire_bonuses.remove(rate_fire_bonus)
                self.refresh_speed += 1

    def u_f_o_iteration(self):
        self.check_u_f_o_collision()

        if random.random() < 0.001 * self.difficult:
            self.create_u_f_o()

        for i in self.u_f_o_list:

            if i.reload_time == 0:
                i.reload_time = i.default_reload_time
                self.u_f_o_shot(i)
            else:
                i.reload_time -= 1 * self.difficult

        self.u_f_o_move_and_draw()

    def create_u_f_o(self):
        v = random.randint(-1, 1)
        if v == 0:
            v = 1
        self.u_f_o_list.append(
            UFO(0, random.randint(0, self.window_height),
                v, 0, 15,
                self.window_width, self.window_width))

    def u_f_o_shot(self, i: UFO):
        c = get_distance(self.player.x, self.player.y, i.x, i.y)
        a = i.x - self.player.x
        b = i.y - self.player.y
        if a > 0 and b > 0:
            i.direction = +math.acos(a / c) + math.pi
        if a > 0 and b <= 0:
            i.direction = -math.acos(a / c) + math.pi
        if a <= 0 and b > 0:
            i.direction = math.acos(a / c) - math.pi
        if a <= 0 and b <= 0:
            i.direction = -math.acos(a / c) - math.pi

        self.shots.append(Shot(i, self.window_width,
                               self.window_height))

    def u_f_o_move_and_draw(self):
        for i in self.u_f_o_list:
            i.draw(pygame, self.window)
            i.move()

    def check_u_f_o_collision(self):
        for u_f_o in self.u_f_o_list:
            for shot in self.shots:
                if get_distance(u_f_o.x, u_f_o.y, shot.x,
                                shot.y) <= u_f_o.size + shot.size:
                    self.shots.remove(shot)
                    self.player.score += 2
                    self.total_score += 2
                    self.u_f_o_list.remove(u_f_o)

    def check_u_f_o_player_collision(self):
        for u_f_o in self.u_f_o_list:
            if get_distance(u_f_o.x, u_f_o.y, self.player.x,
                            self.player.y) <= u_f_o.size + self.player.size:
                self.player.immortal_time = self.default_immortal_time
                return True

    def set_player_default_position(self):
        self.player.x = self.window_width / 2
        self.player.y = self.window_height / 2
        self.player.speed_x = 0
        self.player.speed_y = 0
