from Game import Game


if __name__ == '__main__':
    w = list()
    with open('Asteroids.cfg') as cfg:
        w = cfg.readline().split('x')
    game = Game(int(w[0]), int(w[1]), 0)
    game.start()


