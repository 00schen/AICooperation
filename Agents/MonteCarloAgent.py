import random
from math import pi
from math import cos
from math import sin
from math import atan2
from Point import Point
from Agents.Agent import Agent
from gym.spaces import Discrete


class NaiveAgent(Agent):
    def __init__(self, player, env):
        super().__init__(player, env)


    def select_action(self, state):
        ball = state[-2]
        if state[-1].x == 2 or state[-1].x == 1:
            return (1, self.player.start_pos)
        return (0, self.determine_action(ball))

    def optimize(self):


    
        