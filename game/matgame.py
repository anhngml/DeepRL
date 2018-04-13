from game.env.MatWorldEnv import MatWorldEnv
from game.agent.MatWorldAgent import MWAgent
from game.env.matWorldTarget import MWTarget


class Game:
    def __init__(self, name='MatGame', randMap=False):
        self.finish = False
        self.name = name
        self.env = None
        self.ranMap = randMap

    def new(self):
        try:
            self.finish = False
            self.env = MatWorldEnv(self.ranMap)
            agent = MWAgent(self.env)
            target = MWTarget(self.env, 0, 0)
            self.env.all_targets.append(target)
            self.env.random_put_on(agent)
            self.env.random_put_on(target)
            # self.env.put_on(target, 15, 15)
            self.env.all_agent.append(agent)
        except Exception as e:
            print(e)

    def get_1st_view(self, agentId):
        return self.getAgentById(agentId).observation()

    def getAgentById(self, Id):
        if len(self.env.all_agent) > 0:
            for index, spr in enumerate(self.env.all_agent):
                if spr.Id == Id:
                    return spr
        return False

    def step(self, agentId, action):
        agent = self.getAgentById(agentId)
        if agent is None:
            print('agent\{{}\} not found!'.format(agentId))
        try:
            # if not agent.finish:
            hit, reward = agent.move(action+1)
            return agent.observation(), reward, agent.finish, agent.reward
        except Exception as ex:
            print(action)
            print('agent pos: {},{}'.format(agent.rect.x, agent.rect.y))
            print(agent.targetsInfo)
            print(ex)

    def render(self):
        pass

    def run(self, visual=False):
        max_step = 3
        num_step = 0
        while True:
            num_step += 1
            for agent in self.env.all_agent:
                finish, reward = agent.random_walk()
                if visual:
                    self.env.update_screen()
                print(reward)
                agent.observation()
                if finish:
                    break
            if num_step > max_step:
                break


