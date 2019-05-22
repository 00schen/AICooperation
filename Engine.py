#implements gym.Env

import random
import Soccer
import numpy as np

import gym
from gym import spaces

def make(version):
    if version == "Naive":
        players = lambda : None

    return SoccerEnv(players)

END_CONDITION = lambda x: x >= 1e10
# END_CONDITION = lambda score: score[0] >= 7 or score[1] >= 7

class SoccerEnv(gym.Env):
    def __init__(self, players):
        self.players = players
        self.seed()
        possession = Soccer.TEAM_BLUE \
            if random.randint(0, 1) == 0 \
            else Soccer.TEAM_RED
        self.stage = Soccer.Stage(players(), possession)
        self.steps = 0
        
        self.state = []
        for player in self.stage.players:
            self.state.append(player.center)
        self.state.append(self.stage.ball.center)
        self.state.append(Soccer.Point(0, None))

        self.action_space = spaces.Tuple(
            [spaces.Discrete(4), 
             spaces.Box(low = np.array([0, 0]),
                        high = np.array([Soccer.WIDTH, Soccer.HEIGHT],
                    ))])
    
    def seed(self, seed=None):
        random.seed(seed)

    def bounds(self):
        return [Soccer.WIDTH, Soccer.HEIGHT]

    def step(self, action):
        self.state = self.stage.moveCycle(action)
        reward = []
        for player in self.stage.players:
        #TODO: resolve multiple action types
            pass
        done = END_CONDITION(self.steps)
        return (self.state, reward, done)

    def state(self):
        return self.state

    def reset(self):
        possession = Soccer.TEAM_BLUE \
            if random.randint(0, 1) == 0 \
            else Soccer.TEAM_RED
        self.stage = Soccer.Stage(self.players(), possession)
        self.steps = 0

    def render(self):
        pass

    def close(self):
        pass
        