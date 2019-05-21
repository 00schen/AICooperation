#implements gym.Env

import gym
import random
import soccer

def make(version):
    if version == "Naive":
        players = lambda : None

    return SoccerEnv(players)

class SoccerEnv(gym.Env):
    def __init__(self, players):
        self.players = players
        self.seed()
        possession = soccer.TEAM_BLUE \
            if random.randint(0, 1) == 0 \
            else soccer.TEAM_RED
        self.stage = soccer.Stage(players(), possession)
    
    def seed(self, seed=None):
        random.seed(seed)

    def step(self, action):
        return self.stage.moveCycle(action)

    def reset(self):
        possession = soccer.TEAM_BLUE \
            if random.randint(0, 1) == 0 \
            else soccer.TEAM_RED
        self.stage = soccer.Stage(self.players(), possession)

    def render(self):
        pass

    def close(self):
        pass