from Asteroids.game import Game
import config

if __name__ == '__main__':
    print('Name:')
    name = input()

    scoreboard = list()
    with open("scoreboard.txt") as file:
        for i in range(5):
            line = file.readline()
            if line == "":
                break
            items = line.split()
            scoreboard.append((items[0], int(items[1])))
    game = Game(config.Resolution, 1, config.Difficult, scoreboard, name)

    game.start_level()
