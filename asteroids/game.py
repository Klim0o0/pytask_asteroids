import pygame
import sys
import math
import random
from asteroids.game_objects import Asteroid, Player, Shot, HPBonus, \
    ShieldBonus, RateOfFireBonus, UFO, Bonus, GameObject
from asteroids.menu import Menu
from asteroids.utils import get_distance


class Game:
    def __init__(self, resolution, level: int, difficult: int, scoreboard,
                 name, asteroids=None):
        pygame.init()
        pygame.font.init()
        self.window_width = resolution[0]
        self.window_height = resolution[1]
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        self.menu = Menu(pygame, self.window, self.window_width,
                         self.window_height)

        self.asteroids = asteroids
        self.level = level
        self.difficult = difficult
        self.total_score = 0
        self.scoreboard = scoreboard
        self.name = name
        self.default_immortal_time = 100 / difficult
        self.refresh_time = 0
        self.refresh_speed = 1

        if not asteroids:
            self.asteroids = list()
            self.add_random_asteroid(level * difficult)

        self.player = Player(resolution[0] / 2, resolution[1] / 2, 0, 0, 15,
                             resolution[0], resolution[1])

        self.shots = list()

        self.hp_bonuses = list()
        self.shield_bonuses = list()
        self.rate_fire_bonuses = list()

        self.ufo_list = list()

    def add_random_asteroid(self, asteroids_count: int):
        for i in range(asteroids_count):
            self.asteroids.append(
                Asteroid(int(self.window_width * random.random()),
                         int(self.window_height * random.random()),
                         6 * (random.random() - 0.5),
                         6 * (random.random() - 0.5),
                         12 + int(25 * random.random()), self.window_width,
                         self.window_height))

    def start_level(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 40)
        self.menu.start_menu(font)
        self.player.immortal_time = self.default_immortal_time

        while True:  # основной цикл обработки событий
            clock.tick(60)
            self.window.fill((0, 0, 0))

            if self.check_events():
                self.menu.start_menu(font)

            if self.player.immortal_time > 0:
                self.player.immortal_time -= 1

            self.move()
            self.check_collision()
            self.draw()

            self.ufo_try_shot()
            self.try_create_ufo()

            self.draw_interface()

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

    def draw_interface(self):
        font = pygame.font.Font(None, 32)
        self.window.blit(
            font.render(
                "Score:" + str(self.player.score) + "  Total score:" + str(
                    self.total_score) + "  LVL:" + str(
                    self.level) + "  HP:" + str(self.player.health), 1,
                (255, 255, 255)),
            (10, 5))

    def change_scoreboard(self, file: str):
        offset = 0
        temp_scoreboard = list()
        for i in range(len(self.scoreboard)):
            if i == 5:
                break
            if self.scoreboard[i][1] < self.total_score and offset == 0:
                temp_scoreboard.append((self.name, self.total_score))
                offset = 1
            else:
                temp_scoreboard.append(self.scoreboard[i - +offset])
        self.scoreboard = temp_scoreboard

        line = ""
        for i in self.scoreboard:
            line += i[0] + ' ' + str(i[1]) + '\n'

        with open(file, 'w') as file:
            file.write(line)

    def game_over(self, obj):
        if self.player.immortal_time > 0:
            return
        self.player.health -= 1
        if self.player.health == 0:
            self.change_scoreboard('scoreboard.txt')
            self.menu.start_game_over_screen(pygame.font.Font(None, 40),
                                             self.scoreboard)
            self.__init__((self.window_width, self.window_height), 1,
                          self.difficult, self.scoreboard, self.name)
        else:
            if type(obj) == Shot:
                self.shots.remove(obj)
            self.set_player_default_position()
            self.player.immortal_time = self.default_immortal_time

    def ufo_try_shot(self):
        for ufo in self.ufo_list:
            if ufo.reload_time == 0:
                ufo.reload_time = ufo.default_reload_time
                self.shots.append(ufo.shot(self.player))
            else:
                ufo.reload_time -= 1 * self.difficult

    def try_create_ufo(self):
        if random.random() < 0.001 * self.difficult:
            self.create_ufo()

    def create_bonus(self, game_object):
        r = random.randint(1, 3)
        if r == 1:
            self.hp_bonuses.append(
                HPBonus(game_object, self.window_width, self.window_height,
                        (255, 0, 0)))
        if r == 2:
            self.shield_bonuses.append(
                ShieldBonus(game_object, self.window_width,
                            self.window_height, (0, 255, 0)))
        if r == 3:
            self.rate_fire_bonuses.append(
                RateOfFireBonus(game_object, self.window_width,
                                self.window_height, (0, 0, 255)))

    def create_ufo(self):
        v = random.randint(-1, 1)
        if v == 0:
            v = 1
        self.ufo_list.append(
            UFO(0, random.randint(0, self.window_height),
                v, 0, 30,
                self.window_width, self.window_width))

    def set_player_default_position(self):
        self.player.x = self.window_width / 2
        self.player.y = self.window_height / 2
        self.player.speed_x = 0
        self.player.speed_y = 0

    def delete_asteroid(self, asteroid: Asteroid, shot: Shot):
        self.asteroids.remove(asteroid)
        self.player.score += 1
        self.total_score += 1
        self.shots.remove(shot)
        if random.random() < 0.3:
            self.create_bonus(asteroid)

        if asteroid.size > 15:
            for i in range(3):
                self.asteroids.append(self.create_random_asteroid(asteroid))

    def create_random_asteroid(self, asteroid: Asteroid):
        return Asteroid(asteroid.x, asteroid.y,
                        asteroid.speed_x + 6 * (
                                random.random() - 0.5),
                        asteroid.speed_y + 6 * (
                                random.random() - 0.5),
                        10,
                        self.window_width, self.window_height)

    def delete_ufo(self, ufo: UFO, shot: Shot):
        self.ufo_list.remove(ufo)
        self.player.score += 2
        self.total_score += 2
        self.shots.remove(shot)

    def check_collision(self):
        player_ufo_handle = CollisionHandler.get_handler(Player, UFO)
        player_asteroid_handle = CollisionHandler.get_handler(Player, Asteroid)
        player_shot_handle = CollisionHandler.get_handler(Player, Shot)
        player_bonus_handle = CollisionHandler.get_handler(Player, Bonus)
        asteroid_shot_handle = CollisionHandler.get_handler(Asteroid, Shot)
        ufo_shot_handle = CollisionHandler.get_handler(UFO, Shot)

        for ufo in self.ufo_list:
            player_ufo_handle(self, self.player, ufo)
        for asteroid in self.asteroids:
            player_asteroid_handle(self, self.player, asteroid)

        for shot in self.shots:
            player_shot_handle(self, self.player, shot)
            for ufo in self.ufo_list:
                ufo_shot_handle(self, ufo, shot)
            for asteroid in self.asteroids:
                asteroid_shot_handle(self, asteroid, shot)

        for bonus in self.rate_fire_bonuses:
            player_bonus_handle(self, self.player, bonus)
            if bonus.used:
                self.rate_fire_bonuses.remove(bonus)

        for bonus in self.shield_bonuses:
            player_bonus_handle(self, self.player, bonus)
            if bonus.used:
                self.shield_bonuses.remove(bonus)

        for bonus in self.hp_bonuses:
            player_bonus_handle(self, self.player, bonus)
            if bonus.used:
                self.hp_bonuses.remove(bonus)

    def draw(self):
        self.player.draw(pygame, self.window)
        for ufo in self.ufo_list:
            ufo.draw(pygame, self.window)
        for shot in self.shots:
            shot.draw(pygame, self.window)

        for asteroid in self.asteroids:
            asteroid.draw(pygame, self.window)

        for bonus in self.rate_fire_bonuses:
            bonus.draw(pygame, self.window)

        for bonus in self.shield_bonuses:
            bonus.draw(pygame, self.window)

        for bonus in self.hp_bonuses:
            bonus.draw(pygame, self.window)

    def move(self):
        for ufo in self.ufo_list:
            ufo.move()

        for shot in self.shots:
            if shot.ticks >= 200:
                self.shots.remove(shot)
            else:
                shot.ticks += 1
                shot.move()

        for asteroid in self.asteroids:
            asteroid.move()

        self.player.move()


class CollisionHandler:
    HANDLERS = {
        (Player, Bonus): lambda game, player, bonus: bonus.buff(player),
        (Player, UFO): lambda game, player, ufo: game.game_over(ufo),
        (Player, Shot): lambda game, player, shot: game.game_over(shot),
        (Player, Asteroid): lambda game, player, asteroid: game.game_over(
            asteroid),
        (Asteroid, Shot): lambda game, asteroid, shot: game.delete_asteroid(
            asteroid, shot),
        (UFO, Shot): lambda game, ufo, shot: game.delete_ufo(ufo, shot),
    }

    @staticmethod
    def check_collision(func):
        def wrapper(game: Game, obj_1: GameObject, obj_2: GameObject):
            if get_distance(obj_1.x, obj_1.y, obj_2.x,
                            obj_2.y) <= obj_1.size + obj_2.size:
                func(game, obj_1, obj_2)

        return wrapper

    @classmethod
    def get_handler(cls, obj_1: type(GameObject), obj_2: type(GameObject)):
        try:
            handler = cls.HANDLERS[(obj_1, obj_2)]
            return cls.check_collision(handler)
        except KeyError:
            return lambda game, a, b: None
