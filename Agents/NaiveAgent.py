import random
from math import pi
from math import cos
from math import sin
from math import atan2
import Point

class NaiveAgent(Agent):
    def __init__(self, player, env):
        super().__init__(player, env)
    

    def select_action(self, state):
        ball = state[-2]
        velocity = self.player.max_speed
        p = ball.sub(self.player.center)
        angle = atan2(p.y, p.x)

        if state[-1].x == 2 or state[-1].x == 1:
            return (2, self.__sideReset(state[-2]), velocity, angle)
        elif self.canKick():
            kick = self.player.max_kick
            q = ball.sub(Point(self.goal[0].x,
                        (self.goal[0].y +self.goal[1].y) / 2))
            kick_angle = atan2(q.y, q.x)
            return (1, kick, kick_angle)
        return (0, velocity, angle)

    def __sideReset(self, ball):
        r = random.uniform(10, 30)
        theta = random.uniform(0, 2*pi)
        p = Point(ball.x + r * cos(theta),
                  ball.y + r * sin(theta))
        while (p.x > self.bounds[0] or p.x < 0) \
            or (p.y > self.bounds[1] or p.y < 0):
            r = random.uniform(10, 30)
            theta = random.uniform(0, 2*pi)
            p = Point(ball.x + r * cos(theta),
                      ball.y + r * sin(theta))
        return p
