class Agent:
    def __init__(self, player, env):
        self.player = player
        self.canKick = lambda: \
            env.stage.canKick(self.player)

        self.bounds = env.bounds()
        self.goal = env.stage.getGoal(self.player)

    def select_action(self, state):
        raise NotImplementedError