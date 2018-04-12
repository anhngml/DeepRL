import random
import numpy as np
from collections import deque
import math
import copy


class MWAgent:
    def __init__(self, env):
        super().__init__()
        self.env = env

        self.reward = 0
        self.finish = False

        self.direct = 2
        self.random_direct = 2
        self.Id = 0
        self.trajectory_length = 4
        self.recently_trajectory = deque([], maxlen=self.trajectory_length)
        self.targetsInfo = []
        self.x = 0
        self.y = 0

    def moveRight(self, pixels):
        step_reward = 0
        self.x += pixels
        hit, reward, self.finish = self.env.check_col(self)
        if hit:
            step_reward += reward
            if not self.finish:
                self.x -= pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.direct = 2
        return not hit, step_reward

    def moveLeft(self, pixels):
        step_reward = 0
        self.x -= pixels
        hit, reward, self.finish = self.env.check_col(self)
        if hit:
            step_reward += reward
            if not self.finish:
                self.x += pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.direct = 4
        return not hit, step_reward

    def moveUp(self, pixels):
        step_reward = 0
        self.y -= pixels
        hit, reward, self.finish = self.env.check_col(self)
        if hit:
            step_reward += reward
            if not self.finish:
                self.y += pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.direct = 1
        return not hit, step_reward

    def moveDown(self, pixels):
        step_reward = 0
        self.y += pixels
        hit, reward, self.finish = self.env.check_col(self)
        if hit:
            step_reward += reward
            if not self.finish:
                self.y -= pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.direct = 3
        return not hit, step_reward

    def firstView(self, view_range=5):
        return self.observation(view_range)

    def update_targets_info(self):
        self.targetsInfo = []
        if len(self.env.all_targets) < 1:
            return
        for target in self.env.all_targets:
            c_x = self.x
            c_y = self.y
            t_cx = target.x
            t_cy = target.y
            distance = math.hypot((t_cx - c_x), (t_cy - c_y))
            angle = math.atan2(c_y - t_cy, c_x - t_cx)
            self.targetsInfo.append([distance, angle])

    def observation(self, view_range=5):
        self.update_targets_info()
        res = np.zeros((view_range, view_range))
        cols = int((view_range - 1)/2)
        x0 = self.x - cols
        y0 = self.y - cols
        for i in range(view_range):
            for j in range(view_range):
                xk = x0 + i
                yk = y0 + j
                if 0 <= xk < self.env.mapheight and 0 <= yk < self.env.mapwidth:
                    val = copy.deepcopy(self.env.map[yk][xk])
                else:
                    val = -1
                res[j, i] = val
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #                  for row in res]))
        self.recently_trajectory.append(res)
        while len(self.recently_trajectory) < self.recently_trajectory.maxlen:
            self.recently_trajectory.append(res)
        result = np.array(list(self.recently_trajectory))
        result = np.reshape(result, view_range*view_range*self.trajectory_length)
        result = np.concatenate([result, np.array(self.targetsInfo).flatten()])
        # print(result)
        return result

    def move(self, direct):
        try:
            if self.finish:
                return True, 0
            if direct == 1:
                return self.moveUp(1)
            elif direct == 2:
                return self.moveRight(1)
            elif direct == 3:
                return self.moveDown(1)
            elif direct == 4:
                return self.moveLeft(1)
        except Exception as e:
            print("Error!!!!!!!!")
            print(direct)
            print(self.finish)

            print(e)

    def random_walk(self):
        self.y = 14
        self.x = 13
        self.random_direct = 2
        if self.finish:
            return self.finish, 0
        success, reward = self.move(self.random_direct)
        if not success:
            ran = random.randint(1, 4)
            while ran == self.random_direct:
                ran = random.randint(1, 4)
            self.random_direct = ran
        else:
            p = random.randint(1, 101)
            if p > 95:
                self.random_direct = random.randint(1, 4)
        return False, reward
