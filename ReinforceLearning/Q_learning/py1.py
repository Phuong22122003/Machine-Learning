import gym
env = gym.make("Taxi-v3",render_mode='ansi')
env.reset()
print(env.render())

print("Action Space {}".format(env.action_space))
print("State Space {}".format(env.observation_space))

state = env.encode(0, 2, 2, 0) # (taxi row, taxi column, passenger index, destination index)
print("State:", state)

env.s = state
print(env.render())
env.P[state]


epochs = 0
penalties, reward = 0, 0

frames = [] # for animation
done = False

while not done:
    action = env.action_space.sample()
    
    state, reward, terminated, truncated, info = env.step(action) 
    done = terminated or truncated
    if reward == -10:
        penalties += 1
    
    # Put each rendered frame into dict for animation
    frames.append({
            'frame': env.render(),
            'state': state,
            'action': action,
            'reward': reward
            }
        )

    epochs += 1
    
    
print("Timesteps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))



from IPython.display import clear_output
from time import sleep

def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)
        
# print_frames(frames)



import numpy as np
q_table = np.zeros([env.observation_space.n, env.action_space.n])



#%%time
"""Training the agent"""

import random
from IPython.display import clear_output

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, 100001):
    env.reset()
    state = env.s

    epochs, penalties, reward, = 0, 0, 0
    done = False
    
    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state]) # Exploit learned values
        next_state, reward, terminated, truncated, info = env.step(action) 
        done = terminated or truncated
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1
    if i % 100 == 0:
        #clear_output(wait=True)
        print(f"Episode: {i}")

print("Training finished.\n")

q_table[384]
total_epochs, total_penalties = 0, 0
episodes = 100

for _ in range(episodes):
    env.reset()
    state=env.s
    epochs, penalties, reward = 0, 0, 0
    
    done = False
    
    while not done:
        action = np.argmax(q_table[state])
        state, reward, terminated, truncated, info = env.step(action) 
        done = terminated or truncated

        if reward == -10:
            penalties += 1

        epochs += 1

    total_penalties += penalties
    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")