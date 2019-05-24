import SoccerEnv
from Soccer import Player
import Point
from math import pi

def make(version):
    if version == "Naive":
        players = None
    elif version == "test1":
        players = test1()

    return SoccerEnv(players)

def runSimulation(version):
    env = make(version)
    done = False
    while not done:
        env.render()
    env.close()    

def test1():
    player1 = Player(Point(50,50), 20, 2, 2*pi ,200)
    player2 = Player(Point(30,100), 30, 5, 6, 7)
    return [player1, player2]