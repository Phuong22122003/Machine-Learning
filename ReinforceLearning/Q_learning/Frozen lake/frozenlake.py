import gym
env = gym.make('FrozenLake8x8-v1', desc=None, map_name="4x4", is_slippery=True ,render_mode ="ansi")
env.reset()
print(env.step(3))
state, _, _, _,_= env.step(3)
env.s = state

print("Action space: {}".format(env.action_space))
print("State space: {}".format(env.observation_space))
import numpy as np
q_table = np.zeros((env.observation_space.n, env.action_space.n))
import random

# alpha = 0.1
# gamma = 0.7
# epsilon = 0.9
#
# all_steps = []
# all_rewards = []
#
# for i in range(1, 10000):
#     env.reset()
#     state = env.s
#
#     done = False
#
#     n_step = reward = 0
#
#     while not done:
#         if random.uniform(0, 1) < epsilon:
#             action = env.action_space.sample()
#         else:
#             action = np.argmax(q_table[state])
#         next_state, reward, terminated, truncated,info = env.step(action)
#         done = terminated or truncated
#
#         old_value = q_table[state, action]
#         next_max = np.max(q_table[next_state])
#
#         new_value =  (1 - alpha)*old_value + alpha * (gamma * next_max + reward)
#         q_table[state, action] = new_value
#
#         n_step += 1
#         state = next_state
#
#     if i % 100 == 0:
#         print("Episode: ", i)
#     all_steps.append(n_step)
#     all_rewards.append(reward)
import random

alpha = 0.1
gamma = 0.7
epsilon = 0.7

all_steps = []
all_rewards = []
list_state =[]
for i in range(1, 50000):
    env.reset()
    state = env.s

    done = False

    n_step = reward = 0

    while not done:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state])
        next_state, reward, terminated, truncated,info = env.step(action)
        state_char = env.env.desc.flatten()[next_state]
        if state_char ==b"G":
          reward =10
        elif state_char ==b"H":
          reward =-20
        elif state_char ==b"F":
          reward =-1
        done = terminated

        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_value =  old_value + alpha * (gamma * next_max + reward-old_value)
        q_table[state, action] = new_value

        n_step += 1
        state = next_state

    if i % 100 == 0:
        print("Episode: ", i)
    all_steps.append(n_step)
    all_rewards.append(reward)
episode = 1000
total_steps = 0
total_reward = 0
print(q_table)
penalty =0
for i in range (episode):
    env.reset()
    state = env.s
    done = False
    reward = n_step = 0

    while not done:
        action = np.argmax(q_table[state])
        state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        if done and state!=15:
            penalty+=1

        n_step += 1

    total_steps += n_step
    total_reward += reward
    all_steps.append(n_step)
    all_rewards.append(reward)
print(penalty)
print("Average steps: ", total_steps / episode)
print("Average reward: ", total_reward / episode)