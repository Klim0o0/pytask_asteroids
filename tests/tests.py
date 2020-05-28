import unittest, math, pygame
from unittest.mock import patch
from Asteroids.game_objects import Player, GameObject, Shot, Asteroid
from Asteroids.game import Game
from Asteroids.menu import Menu


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
        self.player.add_speed(1, 1)

        self.assertEqual(self.player.speed_y, 3.5)
        self.assertEqual(self.player.speed_x, 1)


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
        self.game = Game(100, 100, 0, [Asteroid(0, 0, 0, 0, 10, 100, 100)])

    def test(self):
        self.assertTrue(not self.game.check_collision())


class AsteroidPlayerCollisionTrue(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 10, 100, 100)])

    def test(self):
        self.assertTrue(self.game.check_collision())


class AsteroidShotCollision(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.game.shots.append(Shot(self.game.player, 100, 100))

    def test(self):
        self.assertTrue(self.game.check_collision())


class ShotMove(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.shot = Shot(self.game.player, 100, 100)
        self.X = self.shot.x

    def test(self):
        self.shot.move()
        self.assertEqual(self.X + 6, self.shot.x)


class ShotMoveInGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 10, 100, 100)])
        self.game.shots.append(Shot(self.game.player, 100, 100))
        self.X = self.game.shots[0].x

    def test(self):
        self.game.move_shots()
        self.assertEqual(self.X + 6, self.game.shots[0].x)


class CheckEvents(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 10, 100, 100)])

    def test(self):
        self.assertTrue(not self.game.check_events())


class AsteroidShotCollisionTrue(unittest.TestCase):
    def setUp(self):
        self.game = Game(100, 100, 0, [Asteroid(50, 50, 0, 0, 80, 100, 100)])
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
        self.game = Game(100, 100, 0, [])

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


if __name__ == '__main__':
    unittest.main()
