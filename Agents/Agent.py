class Agent:
    def __init__(self, player, env):
        self.player = player
        self.canKick = lambda: \
            env.stage.can_kick(self.player)

        self.bounds = env.bounds()
        self.goal = env.stage.get_goal(self.player)

    def select_action(self, state):
        raise NotImplementedError

    def optimize_model(self, i_episode, done):
        pass
