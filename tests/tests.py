import math
import pygame
import unittest
from unittest.mock import patch

from asteroids.game import Game
from asteroids.game_objects import Player, GameObject, Shot, Asteroid, \
    HPBonus, ShieldBonus, RateOfFireBonus
from asteroids.menu import Menu


class ZeroSpeedMovingTest(unittest.TestCase):
    def setUp(self):
        self.game_object = GameObject(0, 0, 0, 0, 0, 10, 10)

    def test(self):
        self.game_object.move()

        self.assertEqual(self.game_object.x, 0)
        self.assertEqual(self.game_object.y, 0)


class NotZeroSpeedMovingTest(unittest.TestCase):
    def setUp(self):
        self.game_object = GameObject(0, 0, 1, 1, 0, 10, 10)

    def test(self):
        self.game_object.move()

        self.assertEqual(self.game_object.x, 1)
        self.assertEqual(self.game_object.y, 1)


class MovingOutMapTest(unittest.TestCase):
    def setUp(self):
        self.game_object = GameObject(8, 0, 3, 0, 0, 10, 10)

    def test(self):
        self.game_object.move()

        self.assertEqual(self.game_object.x, 1)
        self.assertEqual(self.game_object.y, 0)


class SpeedLimitTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 3.5, 0, 10, 10)

    def test(self):
        self.player.add_speed(83, 1)

        self.assertEqual(self.player.speed_y, 3.5)
        self.assertEqual(self.player.speed_x, 0)


class SpeedAddTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 0, 0, 10, 10)

    def test(self):
        self.player.add_speed(1, 1)

        self.assertEqual(self.player.speed_y, 1)
        self.assertEqual(self.player.speed_x, 1)


class ZeroTurnTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 3.5, 0, 10, 10)

    def test(self):
        self.player.turn_at(0)

        self.assertEqual(self.player.direction, 0)


class NotZeroTurnTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 3.5, 0, 10, 10)

    def test(self):
        self.player.turn_at(1)

        self.assertEqual(self.player.direction, 1)


class MoreTwoPiTurnTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 3.5, 0, 10, 10)

    def test(self):
        self.player.turn_at(10)

        self.assertEqual(self.player.direction, 10 - 2 * math.pi)


class AsteroidPlayerCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(0, 0, 0, 0, 10, 100, 100)])

    def test(self):
        self.assertTrue(not self.game.check_collision())


class AsteroidPlayerCollisionTrue(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 10, 100, 100)])

    def test(self):
        self.game.check_collision()
        self.assertEqual(self.game.player.health, 2)


class AsteroidShotCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.game.shots.append(Shot(self.game.player, 100, 100))
        self.game.shots[0].x = 50
        self.game.shots[0].y = 50
        self.game.player.x = 0
        self.game.player.y = 0

    def test(self):
        self.game.check_collision()
        self.assertEqual(len(self.game.asteroids), 0)


class ShotMove(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.shot = Shot(self.game.player, 100, 100)
        self.X = self.shot.x

    def test(self):
        self.shot.move()
        self.assertEqual(self.X + 6, self.shot.x)


class ShotMoveInGame(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.game.shots.append(Shot(self.game.player, 100, 100))
        self.X = self.game.shots[0].x

    def test(self):
        self.game.move()
        self.assertEqual(self.X + 6, self.game.shots[0].x)


class CheckEvents(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 10, 100, 100)])

    def test(self):
        self.assertTrue(not self.game.check_events())


class AsteroidShotCollisionTrue(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])
        self.game.shots.append(Shot(self.game.player, 100, 100))

    def test(self):
        self.game.check_collision()
        self.assertEqual(len(self.game.shots), 0)
        self.assertEqual(len(self.game.asteroids), 3)


class NextLevelEvents(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((10, 10))
        self.menu = Menu(pygame, self.win, 10, 10)

    def test(self):
        self.assertTrue(not self.menu.check_next_level_events())


class AddRandomAsteroids(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1, [('w', 0)], "", [])

    def test(self):
        self.game.add_random_asteroid(1)
        self.assertEqual(len(self.game.asteroids), 1)


class CheckGameOverEvents(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((10, 10))
        self.menu = Menu(pygame, self.win, 10, 10)

    def test(self):
        self.assertTrue(not self.menu.check_game_over_events())


class ChangeScoreboardTest1(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.change_scoreboard('w.txt')

        self.assertEqual(self.game.scoreboard,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)])


class ChangeScoreboardTest2(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])
        self.game.total_score = 100

    def test(self):
        self.game.change_scoreboard('w.txt')

        self.assertEqual(self.game.scoreboard,
                         [('s', 100), ('w', 1), ('w', 1), ('w', 1), ('w', 1)])


class CreateBotuseTest(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.create_bonus(self.game.asteroids[0])

        self.assertEqual(
            len(self.game.hp_bonuses) + len(self.game.shield_bonuses) + len(
                self.game.rate_fire_bonuses), 1)


class CheckBotuseColisionTest(unittest.TestCase):
    def setUp(self):
        self.game = Game((1000, 1000), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(0, 0, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.hp_bonuses.append(
            HPBonus(self.game.player, 100, 100, (0, 0, 0)))
        self.game.shield_bonuses.append(
            ShieldBonus(self.game.player, 100, 100, (0, 0, 0)))
        self.game.rate_fire_bonuses.append(
            RateOfFireBonus(self.game.player, 100, 100, (0, 0, 0)))
        self.game.check_collision()
        self.assertEqual(self.game.player.health, 4)
        self.assertEqual(self.game.player.immortal_time,
                         self.game.default_immortal_time * 2)
        self.assertEqual(self.game.player.refresh_speed, 2)


class UFOCreateTest(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.create_ufo()
        self.assertEqual(len(self.game.ufo_list), 1)


class UFOShotTest(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.create_ufo()
        self.game.shots.append(self.game.ufo_list[0].shot(self.game.player))
        self.assertEqual(len(self.game.shots), 1)
        self.game.ufo_try_shot()
        self.assertEqual(len(self.game.shots), 2)


class CheckUFOPlayerCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(0, 0, 0, 0, 1, 100, 100)])

    def test(self):
        self.game.create_ufo()
        self.game.player.x = self.game.ufo_list[0].x
        self.game.player.y = self.game.ufo_list[0].y
        self.game.check_collision()
        self.assertTrue(self.game.player.health == 2)


class CheckUFOPCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1), ('w', 1)],
                         "s",
                         [Asteroid(0, 0, 0, 0, 1, 100, 100)])

    def test(self):
        self.game.create_ufo()
        self.game.shots.append(self.game.ufo_list[0].shot(self.game.player))
        self.game.shots[0].x = self.game.ufo_list[0].x
        self.game.shots[0].y = self.game.ufo_list[0].y
        self.game.check_collision()
        self.assertEqual(len(self.game.ufo_list), 0)
        self.assertEqual(self.game.player.score, 2)
        self.assertEqual(len(self.game.shots), 0)


class SetPlayerDefaultPosition(unittest.TestCase):
    def setUp(self):
        self.game = Game((100, 100), 0, 1,
                         [('w', 1), ('w', 1), ('w', 1), ('w', 1),
                          ('w', 1)],
                         "s",
                         [Asteroid(50, 50, 0, 0, 80, 100, 100)])

    def test(self):
        self.game.player.x = 12
        self.game.player.y = 12
        self.game.set_player_default_position()
        self.assertEqual((self.game.player.x, self.game.player.y), (50, 50))


if __name__ == '__main__':
    unittest.main()
