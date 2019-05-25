#Adapted from Pytorch DQN Tutorial:
#https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

import Engine
import math
import random
import numpy as np
from itertools import count

env, agents = Engine.make("Naive")

num_episodes = 50
for i_episode in range(num_episodes):
    # Initialize the environment and state
    env.reset()
    state = env.screen()
    for t in count():
        actions = []
        for agent in agents:
            # Select and perform an action
            actions.append(agent.select_action(state))
        next_state, rewards, done = env.step(actions)
        # rewards = torch.tensor([rewards], device=device)

        if done:
            next_state = None

        for i in range(len(agents)):
            # Store the transition in memory
            agent = agents[i]
            action = actions[i]
            reward = rewards[i]
            agent.memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        for agent in agents:
            # Perform one step of the optimization (on the target network)
            agent.optimize_model(i_episode, done)
        if done:
            break
    
print('Complete')
env.close()
