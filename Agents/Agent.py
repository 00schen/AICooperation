from gym.spaces import Discrete


#Agent needs to know bounds, goal, kick, other player positions, player velocities

class Agent:
    def __init__(self, player, env):
        self.player = player

    def select_action(self, state):
        pass

    def train(self, i_episode, done):
        pass
