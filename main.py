import pygame, sys, math
from pygame.locals import *
import random

pygame.init()
pygame.font.init()
width = 1000
height = 1000
win = pygame.display.set_mode((width, height))


class player:
    def __init__(self, w, h):
        self.x = w / 2
        self.y = w / 2
        self.direction = 0
        self.speed_x = 0
        self.speed_y = 0
        self.score = 0
        pass

    def move(self):
        self.y = (self.y + self.speed_y) % 1000
        self.x = (self.x + self.speed_x) % 1000

    def draw(self):
        global pygame, win
        direction = self.direction + math.pi
        x = self.x - 17 * math.cos(direction)
        y = self.y - 17 * math.sin(direction)
        pygame.draw.line(win, (255, 255, 255), (x, y),
                         ((x + math.cos(direction - math.pi / 12) * 38), (y + math.sin(direction - math.pi / 12) * 38)),
                         1)
        pygame.draw.line(win, (255, 255, 255), (x, y),
                         ((x + math.cos(direction + math.pi / 12) * 38), (y + math.sin(direction + math.pi / 12) * 38)),
                         1)
        pygame.draw.line(win, (255, 255, 255),
                         ((x + math.cos(direction - math.pi / 12) * 32), (y + math.sin(direction - math.pi / 12) * 32)),
                         ((x + math.cos(direction + math.pi / 12) * 32), (y + math.sin(direction + math.pi / 12) * 32)),
                         1)

    def turn_at(self, angle: float):
        self.direction = (self.direction + angle) % (2 * math.pi)

    def add_speed(self, speed_x: float, speed_y: float):
        if 5 > math.fabs(self.speed_x + speed_x):
            self.speed_x += speed_x
        if 5 > math.fabs(self.speed_y + speed_y):
            self.speed_y += speed_y


class asteroid:
    def __init__(self, x: object, y: object, speed_x: object, speed_y: object, r: object) -> object:
        self.speed_y = speed_y
        self.size = r
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.y = (self.y + self.speed_y) % 1000
        self.x = (self.x + self.speed_x) % 1000
        pass

    def draw(self):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.size - 1)


class shot:
    def __init__(self, p: player):
        direction = p.direction
        self.x = p.x - 15 * math.cos(direction + math.pi)
        self.y = p.y - 15 * math.sin(direction + +math.pi)
        self.speed_x = 5 * math.cos(direction)
        self.speed_y = 5 * math.sin(direction)
        self.ticks = 0

    def move(self):
        self.y = (self.y + self.speed_y) % 1000
        self.x = (self.x + self.speed_x) % 1000

    def draw(self):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x - 2), int(self.y - 2)), 2)


def get_distance(x1: float, y1: float, x2: float, y2: float):
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x * x + y * y)


class game:
    global width, height
    i = 0
    w = 500
    p = player(width, height)
    shots = []
    asteroids = list()

    fl = True

    def __init__(self, asteroids: asteroid):
        self.asteroids = asteroids
        self.win = win
        pass

    def start(self):
        clock = pygame.time.Clock()
        sc = 0
        while self.fl:  # основной цикл обработки событий
            clock.tick(60)
            self.win.fill((0, 0, 0))

            self.w += 1
            a = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            v = pygame.key.get_pressed()
            if v[pygame.K_LEFT]:
                self.p.turn_at(0.1)
            if v[pygame.K_RIGHT]:
                self.p.turn_at(-0.1)
            if v[pygame.K_SPACE]:
                self.p.add_speed(0.05 * -math.cos(self.p.direction + math.pi),
                                 0.05 * - math.sin(self.p.direction + math.pi))
            if v[pygame.K_UP]:
                if sc <= 0:
                    self.shots.append(shot(self.p))
                    sc = 20
                pass

            if sc > 0:
                sc -= 1
            for i in self.shots:
                i.move()
                i.draw()
                i.ticks += 1
                if i.ticks >= 12пп0:
                    self.shots.remove(i)

            for j in self.asteroids:
                for i in self.shots:
                    if get_distance(j.x, j.y, i.x, i.y) < 26:
                        self.shots.remove(i)
                        self.p.score += 1
                        self.asteroids.remove(j)
                        if j.size > 15:
                            self.asteroids.append(asteroid(j.x, j.y, j.speed_x+2, j.speed_y+1, 10))
                            self.asteroids.append(asteroid(j.x, j.y, j.speed_x+1, j.speed_y-2, 10))
                            self.asteroids.append(asteroid(j.x, j.y, j.speed_x-2, j.speed_y+1, 10))

            self.p.move()
            self.p.draw()
            for i in self.asteroids:
                i.move()
                i.draw()
                if get_distance(self.p.x, self.p.y, i.x, i.y) < 26:
                    self.win.fill((0, 0, 0))

                    self.fl = False
            font = pygame.font.Font(None, 32)
            r = font.render(str(self.p.score), 1, (255, 255, 255))
            win.blit(r, (10, 5))
            pygame.display.update()
            if len(self.asteroids)==0:
                return True
        return False


def main():

    font = pygame.font.Font(None, 51)
    r = font.render(u'Press space to start', 2, (255, 255, 255))
    win.blit(r, (350, 500))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        v = pygame.key.get_pressed()
        if v[pygame.K_SPACE]:
            break

    g = game([asteroid(300, 500, 1, 2, 27),asteroid(200, 100, 4, 2, 31),asteroid(7, 6, 1, 1.2, 11),asteroid(52, 6, 4, 1.2, 35)])
    if g.start():
        r = font.render(u'You win', 2, (255, 255, 255))
        win.fill((0, 0, 0))
        win.blit(r, (420, 500))
    else:
        r = font.render(u'Game over', 2, (255, 255, 255))
        win.fill((0, 0, 0))
        win.blit(r, (400, 500))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    pass


if __name__ == '__main__':
    main()
