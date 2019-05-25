# Adapted from pygame.draw tutorial:
# https://www.pygame.org/docs/ref/draw.html

import pygame
from pygame import draw
from Soccer import *
from Point import Point

# Define the colors we will use in RGB format
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
BLUE =   (  0,   0, 255)
GREEN =  (  0, 255,   0)
RED =    (255,   0,   0)
YELLOW = (255, 255,   0)

ENLARGE = 3
XBUFFER = 10
YBUFFER = 10


class Renderer:
    def __init__(self, stage):
        size = [ENLARGE * WIDTH + 2*XBUFFER,
                ENLARGE * HEIGHT + 2*YBUFFER]
        self.screen = pygame.display.set_mode(size)
        self.stage = stage

    def regular_cycle(self):
        done = False
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Clear the screen and set the screen background
        self.screen.fill(WHITE)

        # Draw players
        for player in self.stage.players:
            point = Renderer.__translate(player.center)
            if player.team == TEAM_BLUE:
                draw.circle(self.screen, BLUE, point, player.radius)
            else:
                draw.circle(self.screen, RED, point, player.radius)

        # Draw ball
        ball = self.stage.ball
        point = Renderer.__translate(ball.center)
        draw.circle(self.screen, GREEN, point, ball.radius)

        # Draw borders
        r = Renderer.__translate(Point(0, HEIGHT)) + (WIDTH*ENLARGE, HEIGHT*ENLARGE)
        draw.rect(self.screen, BLACK, r, 2)

        # Draw goal
        g1, g2 = self.stage.walls[2].inner, self.stage.walls[3].inner
        gg1, gg2 = [0, 0], [0, 0]
        for i in range(2):
            gg1[i], gg2[i] = Renderer.__translate(g1[i]), Renderer.__translate(g2[i])
        draw.line(self.screen, YELLOW, *gg1, 2)
        draw.line(self.screen, YELLOW, *gg2, 2)
        
        pygame.display.flip()
        return done

    def __translate(p):
        p = p.mult(3)
        p = p.add(Point(XBUFFER, YBUFFER))
        return (int(p.x), int(p.y))
