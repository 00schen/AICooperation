# implements gym.Env
# TODO: work out action_space
# TODO: make random non-repetitive

import random
from Soccer import *
import numpy as np
from math import fabs

import gym
from gym import spaces

import pygame
from Renderer import Renderer
from Point import Point


END_CONDITION = lambda x: x >= 1e10
# END_CONDITION = lambda score: score[0] >= 7 or score[1] >= 7

WIDTH = 400
HEIGHT = 200

TEAM_RED = 1
TEAM_BLUE = 2


class SoccerEnv(gym.Env):
    """ 
    Only ONE instance is supposed to run at a time
    """
    def __init__(self, players):
        pygame.init()

        self.players = players
        self.seed()
        self.stage = Stage()
        self.steps = 0

        self.action_space = spaces.Discrete(4)
        self.discrete_space = spaces.Box(low=np.array([0, 0]), 
            high=np.array([WIDTH / 4, HEIGHT / 4]), dtype=int)
        self.continuous_space = spaces.Box(low=np.array([0, 0]),
            high=np.array([WIDTH, HEIGHT]))

        self.renderer = Renderer(self.stage)
        self.clock = pygame.time.Clock()
    
    def seed(self, seed=None):
        random.seed(seed)

    def step(self, actions):
        self.steps += 1

        game_state = self.stage.move_cycle(actions, self.players)
        reward = []
        for player in self.players:
            reward.append(self.reward(player, self.state[-1]))
        
        # stage needs to give feedback if ball is scored.

        return self.state, reward, done

    def screen(self):
        return self.state

    def reset(self):
        self.stage = Stage()
        self.steps = 0
        self.clock = pygame.time.Clock()

    def render(self):
        self.clock.tick(3)
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

class Stage:
    def __init__(self):
        bounds = [Point(0, 0), Point(WIDTH, 0), Point(0, HEIGHT), Point(WIDTH, HEIGHT)]
        # Blue goal is walls[2] (Left), Red goal is walls[3] (Right)
        self.walls = [
            Wall((bounds[0], bounds[1])), Wall((bounds[2], bounds[3])),
            Goal((bounds[0], bounds[2]),
                 (Point(0, HEIGHT / 3), Point(0, HEIGHT * 2 / 3))),
            Goal((bounds[1], bounds[3]),
                 (Point(WIDTH, HEIGHT / 3), Point(WIDTH, HEIGHT * 2 / 3)))
        ]
        self.ball = Ball(Point(WIDTH / 2, HEIGHT / 2))
        self.possession = (TEAM_BLUE, TEAM_RED)[random.randint(0, 1) == 0]
        self.score = [0, 0]

    def move_cycle(self, actions, players):
        """
        Returns new state of game.
        0 - continue
        1 - goal scored
        2 - penalty
        """

        for i in range(len(players)):
            player = players[i]
            action = actions[i]
            player.move(action)
            for other in players:
                if Circle.collide(player, other) and player != other:
                    player.revert_move()
            if Circle.collide(player, self.ball):
                self.possession = player.team
                self.ball.move(player)

        self.ball.move()
        scored = self.__ball_scored()
        if scored:
            self.ball.replace()
            if scored == TEAM_RED:
                self.score[1] += 1
                return (1, TEAM_RED)
            else:
                self.score[0] += 1
                return (1, TEAM_BLUE)
        elif self.__ball_out_bounds():
            if self.possession == TEAM_BLUE:
                self.ball.restart(Point(WIDTH / 4, HEIGHT / 2))
            else:
                self.ball.restart(Point(WIDTH * 3/4, HEIGHT / 2))
            return (2, self.possession)
        else:
           return (0, None)

    def __ball_scored(self):
        if self.walls[2].has_scored(self.ball) \
                or self.ball.center.x < 0:
            return TEAM_RED
        elif self.walls[3].has_scored(self.ball) \
                or self.ball.center.x > WIDTH:
            return TEAM_BLUE
        else:
            return 0

    def __ball_out_bounds(self): 
        return self.walls[0].collide(self.ball) \
            or self.walls[1].collide(self.ball) \
            or self.walls[2].collide(self.ball) \
            or self.walls[3].collide(self.ball)

class Wall:
    HORIZONTAL = 1
    VERTICAL = 2
    def __init__(self, bounds):
        self.bounds = bounds
        if bounds[0].x == bounds[1].x:
            self.orientation = VERTICAL
        else:
            self.orientation = HORIZONTAL

    def collide(self, c):
        if self.orientation == HORIZONTAL:
            # Check y values
            return fabs(c.center.y - self.bounds[0].y) <= c.radius
        else:
            # Check x values
            return fabs(c.center.x - self.bounds[0].x) <= c.radius
    
    def __str__(self):  # Good
        return "Bound 1: {}\nBound 2: {} \nOrientation: {}"\
            .format(self.bounds[0], self.bounds[1], self.orientation)

class Goal(Wall):
    def __init__(self, bounds, net):  # Good
        super().__init__(bounds)
        self.net = net

    def has_scored(self, b):  # Good
        # check if b is within bounds
        bound1 = min(self.net[0].y, self.net[1].y)
        bound2 = max(self.net[0].y, self.net[1].y)
        within_bounds = b.center.y >= bound1 and b.center.y <= bound2
        return net.collide(b) and within_bounds

    def collide(self, b):  # Good
        return super().collide(b) and not self.has_scored(b)
    
    def __str__(self):  # Good
        return super().__str__() + "\nGoal bound 1: {}\nGoal bound 2: {}"\
            .format(self.net[0], self.net[1])

class Circle:
    def __init__(self, center, radius):  # Good
        self.start_pos = center
        self.center = center
        self.radius = radius
        self.x_vel = 0
        self.y_vel = 0

    def move(self):  # Good
        dp = Point(self.x_vel, self.y_vel)
        self.center = self.center.add(dp)

    def collide(c0, c1):
        return Point.normSq(c0.center, c1.center) \
            <= (c0.radius + c1.radius)**2

    def restart(self, center):
        self.center = center
        self.x_vel, self.y_vel = 0, 0

    def __str__(self):  # Good
        return "\nCenter: {} \nRadius: {}"\
            .format(self.center, self.radius)

class Ball(Circle):
    def __init__(self, center):  # Good
        super().__init__(center, 5)

    def move(self, player):
        # fix this
        """momentum-based kicking"""
        player_mass = .5
        delx, dely = random.random(), random.random()
        self.x_vel += player_mass*player.x_vel + delx
        self.y_vel += player_mass*player.y_vel + dely

class Player(Circle):
    def __init__(self, center, max_speed, team):  # Good
        super().__init__(center, 20)
        self.max_speed_sq = max_speed**2
        self.prev_pos = center
        self.team = team        

    def revert_move(self):  # Good
        self.center = self.prev_pos

    def move(self, action):  # Good
        """takes 'direction key' input"""
        if action == 0:
            dx, dy = 0, 1
        elif action == 1:
            dx, dy = 1, 0
        elif action == 2:
            dx, dy = 0, -1
        elif action == 3:
            dx, dy = -1, 0
        else:
            dx, dy = 0, 0

        # Check for max speed
        if ((self.vel_x + dx)**2 + (self.vel_y + dy)**2) \
            <= self.max_speed_sq:
            self.x_vel += dx
            self.y_vel += dy

        self.prev_pos = self.center
        super(Player, self).move()
        
    def __str__(self):  # Good
        return super(Player, self).__str__() + "\nMax Speed: {} \n Team: {}"\
            .format(self.max_speed_sq**.5, self.team)
