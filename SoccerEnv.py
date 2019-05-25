# implements gym.Env
# TODO: work out action_space

import random
from Soccer import *
import numpy as np

import gym
from gym import spaces

import pygame
from Renderer import Renderer
from Point import Point

END_CONDITION = lambda x: x >= 1e10
# END_CONDITION = lambda score: score[0] >= 7 or score[1] >= 7


class SoccerEnv(gym.Env):
    """ 
    Only ONE instance is supposed to run at a time
    """
    def __init__(self, players):
        pygame.init()

        self.players = players
        self.seed()
        possession = (TEAM_BLUE, TEAM_RED)[random.randint(0, 1) == 0]
        self.stage = Stage(players, possession)
        self.steps = 0
        
        self.state = []
        for player in self.stage.players:
            self.state.append(player.center)
        self.state.append(self.stage.ball.center)
        self.state.append(Point(0, None))

        # self.action_space = spaces.Tuple(
        #     [spaces.Discrete(4), 
        #      spaces.Box(low = np.array([0, 0]),
        #                 high = np.array([WIDTH, HEIGHT],
        #             ))])

        self.renderer = Renderer(self.stage)
        self.clock = pygame.time.Clock()

    def players(self):
        return self.stage.players
    
    def seed(self, seed=None):
        random.seed(seed)

    def bounds(self):
        return [WIDTH, HEIGHT]

    def step(self, actions):
        self.steps += 1
        self.state = self.stage.move_cycle(actions)
        reward = []
        for player in self.stage.players:
            reward.append(self.reward(player, self.state[-1]))
        done = END_CONDITION(self.steps)
        return self.state, reward, done

    def screen(self):
        return self.state

    def reset(self):
        possession = (TEAM_BLUE, TEAM_RED)[random.randint(0, 1) == 0]
        self.stage = Stage(self.players(), possession)
        self.steps = 0
        self.clock = pygame.time.Clock()

    def render(self):
        self.clock.tick(10)
        return self.renderer.regular_cycle()

    def close(self):
        pygame.quit()
        
    def reward(self, player, response):
        if response.x == 1:
            if response.y == player.team:
                return -100
            else:
                return 100
        elif response.x == 2:
            if response.y == player.team:
                return -100
            else:
                return 0
        else:
            if response.y == player.team:
                return 1
            else:
                return -1
