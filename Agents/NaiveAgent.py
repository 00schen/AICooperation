import random
from math import pi
import Point

class NaiveAgent(Agent):
    def __init__(self, env, player):
        self.player = player
        self.bounds = env.bounds()
        self.canKick = lambda: \
            env.stage.canKick(self.player)
    

    def select_action(self, state):
        velocity = self.player.max_speed
        angle = random.uniform(0, 2*pi)

        if state[-1].x == 2 or state[-1].x == 1:
            x = random.uniform(0, self.bounds[0])
            y = random.uniform(0, self.bounds[1])
            return (3, Point(x, y), velocity, angle)
        elif self.canKick():
            kick = random.uniform(0, self.player.max_kick)
            kick_angle = random.uniform(0, self.player.max_angle)
            return (2, kick, kick_angle)
        
        move = random.randint(0, 1)
        return (0) if move == 0 else (1, velocity, angle)



