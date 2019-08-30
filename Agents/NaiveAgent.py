import random
from math import pi
from math import cos
from math import sin
from math import atan2
from Point import Point
from Agents.Agent import Agent


class NaiveAgent(Agent):
    def __init__(self, player, env):
        super().__init__(player, env)

    def select_action(self, state):
        ball = state[-2]
        if state[-1].x == 2 or state[-1].x == 1:
            return (1, self.player.start_pos)
        return (0, self.determine_action(ball))

    # def __side_reset(self, ball):
    #     r = random.uniform(10, 30)
    #     theta = random.uniform(0, 2*pi)
    #     p = Point(ball.x + r * cos(theta),
    #               ball.y + r * sin(theta))
    #     while (p.x > self.bounds[0] or p.x < 0) \
    #             or (p.y > self.bounds[1] or p.y < 0):
    #         r = random.uniform(10, 30)
    #         theta = random.uniform(0, 2*pi)
    #         p = Point(ball.x + r * cos(theta),
    #                   ball.y + r * sin(theta))
    #     return p

    def determine_action(self, ball):
        speed_sq = self.player.x_vel**2 + self.player.y_vel**2
        vel_angle = atan2(self.player.y_vel, self.player.x_vel)
        q = self.player.center.sub(ball)
        ball_dist_sq = q.x**2 + q.y**2
        ball_angle = atan2(q.y, q.x)
        print(vel_angle)
        print(ball_angle)
        if ball_dist_sq <= 200 and speed_sq > 100:
            if vel_angle < ball_angle:
                if vel_angle <= pi and vel_angle > pi / 2:
                    return 3
                elif vel_angle <= pi / 2 and vel_angle > 0:
                    return 4
                elif vel_angle <= 0 and vel_angle > pi / -2:
                    return 1
                else:
                    return 2
            elif vel_angle > ball_angle or speed_sq < 1:
                if vel_angle <= pi and vel_angle > pi / 2:
                    return 2
                elif vel_angle <= pi / 2 and vel_angle > 0:
                    return 3
                elif vel_angle <= 0 and vel_angle > pi / -2:
                    return 4
                else:
                    return 1
        else:
            if vel_angle < ball_angle:
                if vel_angle <= pi and vel_angle > pi / 2:
                    return 4
                elif vel_angle <= pi / 2 and vel_angle > 0:
                    return 1
                elif vel_angle <= 0 and vel_angle > pi / -2:
                    return 2
                else:
                    return 3
            elif vel_angle > ball_angle or speed_sq < 1:
                if vel_angle <= pi and vel_angle > pi / 2:
                    return 1
                elif vel_angle <= pi / 2 and vel_angle > 0:
                    return 2
                elif vel_angle <= 0 and vel_angle > pi / -2:
                    return 3
                else:
                    return 4
