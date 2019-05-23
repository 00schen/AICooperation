#Probably not going to be used

import random
from math import pi
import Point

class RandomAgent(Agent):
    def __init__(self, player, env):
        super().__init__(player, env)
    

    def select_action(self, state):
        velocity = random.uniform(0, self.player.max_speed)
        angle = random.uniform(0, 2*pi)

        if state[-1].x == 2 or state[-1].x == 1:
            x = random.uniform(0, self.bounds[0])
            y = random.uniform(0, self.bounds[1])
            return (2, Point(x, y), velocity, angle)
        elif self.canKick():
            kick = random.uniform(0, self.player.max_kick)
            kick_angle = random.uniform(0, self.player.max_angle)
            return (1, kick, kick_angle)
        
        return (0, velocity, angle)