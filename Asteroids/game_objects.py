from abc import ABC, abstractmethod
import math


class GameObject:

    def __init__(self, x: float, y: float, speed_x: float, speed_y: float,
                 r: float, window_width: int, window_height: int):
        self.speed_y = speed_y
        self.size = r
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.score = 0
        self.direction = 0
        self.window_width = window_width
        self.window_height = window_height

    def move(self):
        self.y = (self.y + self.speed_y) % self.window_height
        self.x = (self.x + self.speed_x) % self.window_width

    @abstractmethod
    def draw(self, pygame, win):
        pass

    def add_speed(self, speed_x: float, speed_y: float):
        if 4 > abs(self.speed_x + speed_x):
            self.speed_x += speed_x
        if 4 > abs(self.speed_y + speed_y):
            self.speed_y += speed_y

    def turn_at(self, angle: float):
        self.direction = (self.direction + angle) % (2 * math.pi)


class Player(GameObject, ABC):

    def draw(self, pygame, win):
        direction = self.direction + math.pi
        x = self.x - 17 * math.cos(direction)
        y = self.y - 17 * math.sin(direction)
        pygame.draw.resolution(win, (255, 255, 255), (x, y),
                               ((x + math.cos(direction - math.pi / 12) * 38),
                          (y + math.sin(direction - math.pi / 12) * 38)),
                               1)
        pygame.draw.resolution(win, (255, 255, 255), (x, y),
                               ((x + math.cos(direction + math.pi / 12) * 38),
                          (y + math.sin(direction + math.pi / 12) * 38)),
                               1)
        pygame.draw.resolution(win, (255, 255, 255),
                               ((x + math.cos(direction - math.pi / 12) * 32),
                          (y + math.sin(direction - math.pi / 12) * 32)),
                               ((x + math.cos(direction + math.pi / 12) * 32),
                          (y + math.sin(direction + math.pi / 12) * 32)),
                               1)


class Asteroid(GameObject, ABC):

    def draw(self, pygame, win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)),
                           self.size)
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)),
                           self.size - 1)


class Shot(GameObject):
    def __init__(self, p: Player, window_width: int, window_height: int):
        super().__init__(p.x - 20 * math.cos(p.direction + math.pi),
                         p.y - 20 * math.sin(p.direction + +math.pi),
                         6 * math.cos(p.direction), 6 * math.sin(p.direction),
                         2,
                         window_width, window_height)
        self.ticks = 0

    def draw(self, pygame, win):
        pygame.draw.circle(win, (255, 255, 255),
                           (int(self.x - 2), int(self.y - 2)), 2)
