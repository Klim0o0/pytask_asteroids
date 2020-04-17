import unittest, math
from GameObjects import GameObject, Player, Asteroid
from Game import Game


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


class SpeedLimitTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 0, 0, 3.5, 0, 10, 10)

    def test(self):
        self.player.add_speed(1, 1)

        self.assertEqual(self.player.speed_y, 3.5)
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
        self.assert_(not self.game.check_collision())


if __name__ == '__main__':
    unittest.main()
