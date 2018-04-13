from game.game import Game
from game import matgame


class myEnv:
    def __init__(self, visual=False, game='GridWorld'):
        self.visual = visual
        self.observation_space_shape = 5*5*4 + 2*1  # [32*5, 32*5, 3]
        self.action_space = [1, 2, 3, 4]
        if game == 'MatWorld':
            self.game = matgame.Game(randMap=True)
        else:
            self.game = Game(trainingMode=True, rootFol='', visual=self.visual, name=game)

    def reset(self):
        self.game.new()
        # self.game.run()
        self.game.render()
        return self.game.get_1st_view(0)

    def step(self, action):
        return self.game.step(0, action)


def make(visual=True, game='GridWorld'):
    return myEnv(visual, game)
