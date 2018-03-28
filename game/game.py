import pygame, random
from game.env.env import Env
from game.agent.agent import Agent
import cv2


class Game:
    def __init__(self, trainingMode=False, rootFol='', visual=True):
        pygame.init()
        pygame.font.init()

        self.finish = False
        self.trainingMode = trainingMode
        self.visual = visual

        SCREENWIDTH = 512
        SCREENHEIGHT = 512

        self.screen_size = (SCREENWIDTH, SCREENHEIGHT)
        if self.visual:
            self.screen = pygame.display.set_mode(self.screen_size)
        else:
            self.screen = pygame.display.set_mode((1, 1))
        self.background = pygame.Surface(self.screen_size)
        pygame.display.set_caption("DeepRL")
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 16)
        self.rootFol = rootFol

    def new(self):
        self.all_agent = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        self.env = Env(self.rootFol)
        self.all_agent.add(Agent(self.env, self.trainingMode, self.rootFol))
        self.render()

    def get_1st_view(self, agentId):
        return self.getAgentById(agentId).firstView(self.background)

    def getAgentById(self, Id):
        for index, spr in enumerate(self.all_agent):
            if spr.Id == Id:
                return spr
        return False

    def step(self, agentId, action):
        agent = self.getAgentById(agentId)
        if agent is None:
            print('agent\{{}\} not found!'.format(agentId))
        hit, reward = agent.move(action+1)
        if self.trainingMode:
            self.update_screen()
        return agent.firstView(self.background), reward, agent.finish, agent.reward

    def render(self):
        self.env.refresh(self.background)
        if self.visual:
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def update_screen(self):
        if self.visual:
            self.screen.blit(self.background, (0, 0))
            self.all_agent.draw(self.screen)
            for agent in self.all_agent:
                agent.updateReward(self.myfont, self.screen)
            pygame.display.flip()

    def run(self, random_move=False):
        self.render()
        carryOn = True
        while carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
            keys = pygame.key.get_pressed()
            for s in self.all_agent:
                if keys[pygame.K_LEFT]:
                    s.move(4)
                if keys[pygame.K_RIGHT]:
                    s.move(2)
                if keys[pygame.K_UP]:
                    s.move(1)
                if keys[pygame.K_DOWN]:
                    s.move(3)
            if random_move:
                for agent in self.all_agent:
                    if not self.trainingMode:
                        agent.random_walk()
                        cv2.imshow('1st view', agent.firstView(self.background))
                        cv2.waitKey(1)
                    if agent.finish:
                        self.finish = True
            self.update_screen()
            self.clock.tick(60)
        pygame.quit()




