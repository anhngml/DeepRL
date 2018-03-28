from game.game import Game


class myEnv:
    def __init__(self, visual=False):
        self.visual = visual
        self.observation_space_shape = [32*5, 32*5, 3]
        self.action_space = [1, 2, 3, 4]
        self.game = Game(trainingMode=True, rootFol='', visual=self.visual)


    def reset(self):
        self.game.new()
        # self.game.run()
        self.game.render()
        return self.game.get_1st_view(0)

    def step(self, action):
        return self.game.step(0, action)


def make(visual=True):
    return myEnv(visual)
