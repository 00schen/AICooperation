#Adapted from Pytorch DQN Tutorial:
#https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

import Engine
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from itertools import count

# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

env = Engine.make("Naive")
players = env.players()

num_episodes = 50
for i_episode in range(num_episodes):
    # Initialize the environment and state
    env.reset()
    state = env.state()
    for t in count():
        actions = []
        for player in players:
            # Select and perform an action
            actions.append(player.select_action(state))
        _, rewards, done = env.step(actions)
        # rewards = torch.tensor([rewards], device=device)

        if not done:
            next_state = env.state()
        else:
            next_state = None

        for i in range(len(players)):
            # Store the transition in memory
            player = players[i]
            action = actions[i]
            reward = rewards[i]
            player.memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        for player in players:
            # Perform one step of the optimization (on the target network)
            player.optimize_model(i_episode, done)
        if done:
            break
    
print('Complete')
env.render()
env.close()
