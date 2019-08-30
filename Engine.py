from SoccerEnv import SoccerEnv
from Soccer import *
from Point import Point
from Agents.NaiveAgent import NaiveAgent


def make(version):
    env, agents = None, None
    if version == "Naive":
        env, agents = None, None
    elif version == "test1":
        env, agents = test1()

    return env, agents


def run_simulation(version):
    env, agents = make(version)
    done = False
    state = env.screen()

    while not done:
        actions = []
        for agent in agents:
            # Select and perform an action
            actions.append(agent.select_action(state))
        print(actions)
        print(state)
        state, _, done = env.step(actions)

        done = env.render()
    env.close()    


def test1():
    player1 = Player(Point(WIDTH / 3, HEIGHT / 2), 10, TEAM_BLUE)
    player2 = Player(Point(WIDTH * 2 / 3, HEIGHT / 2), 10, TEAM_RED)
    env = SoccerEnv([player1, player2])
    agent1 = NaiveAgent(player1, env)
    agent2 = NaiveAgent(player2, env)
    return env, (agent1, agent2)


run_simulation("test1")
