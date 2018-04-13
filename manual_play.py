from game.matgame import Game

if __name__ == "__main__":
    g = Game(name='MatWorld', randMap=True)
    while True:
        g.new()
        g.run(True)

