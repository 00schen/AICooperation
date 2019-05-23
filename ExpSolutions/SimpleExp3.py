#Adapted from Pytorch DQN Tutorial:
#https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

import ExpSolutions.ExpSolution
import random
import math

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200

class SimpleExp3(ExpSolution):
    def __init__(self):
        self.steps_done = 0

    def decision():
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
            math.exp(-1. * steps_done / EPS_DECAY)
        self.steps_done += 1
        return sample > eps_threshold
        