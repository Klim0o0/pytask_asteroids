from Asteroids.game import Game

if __name__ == '__main__':
    with open('Asteroids.cfg') as cfg:
        line = cfg.readline().split(' ')
        resolution = line[1].split('x')
    game = Game(int(resolution[0]), int(resolution[1]), 0)
    game.start()


