#Adapted from pygame.draw tutorial:
#https://www.pygame.org/docs/ref/draw.html

import pygame
from pygame import draw
from Soccer import *

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
        size = [ENLARGE * WIDTH + 2*XBUFFER, \
                ENLARGE * HEIGHT + 2*YBUFFER]
        self.screen = pygame.display.set_mode(size)
        self.stage = stage

    def regularCycle(self, clock):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        # Draw players
        for player in self.stage.players:
            point = __translate(player.center)   
            if player.team == TEAM_BLUE:
                draw.circle(screen, BLUE, point, player.radius)
            else:
                draw.circle(screen, RED, point, player.radius)

        # Draw ball
        ball = self.stage.ball
        point = __translate(ball.center)
        draw.circle(screen, GREEN, point, ball.radius)

        # Draw borders
        r = pygame.Rect(__translate(self.stage.borders[2]),
                        (WIDTH, HEIGHT))
        draw.rect(screen, BLACK, r, 2)

        # Draw goal
        g1, g2 = stage.walls[2].inner, stage.walls[3].inner
        for i in range(2):
            g1[i], g2[i] = __translate(g1[i]), __translate(g2[i])
        draw.line(screen, YELLOW, *g1, 2)
        draw.line(screen, YELLOW, *g2, 2)
        
        pygame.display.flip()

    def __translate(p):
        p = p.mult(3)
        p = p.add(Point(XBUFFER, YBUFFER))
        return (p.x, p.y)
        
