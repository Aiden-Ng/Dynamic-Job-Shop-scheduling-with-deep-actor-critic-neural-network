import gym
import JSSEnv
import os 
import numpy as np
import inspect

# for i in gym.envs.registry.keys():
#     print(i)

INSTANCE_PATH = r"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\JSSEnv\envs\instances\ta01"

env = gym.make('jss-v1',  env_config={'instance_path': INSTANCE_PATH})
#env = gym.make('jss-v1')

#Q : do i have to reset everytime?
#A : Yes, you have to reset the environment everytime you want to start a new episode.
seed = 1 
# env = JSSEnv()

obs, info = env.reset() #not sure why cannot add seed here

# print("Initial Observation:", obs)
# print("Additional Info:", info)
# print(len(obs["real_obs"][0]))
# print(obs["action_mask"])
print("=======================Start of the program=======================")
print(env.action_space)
print(type(env.action_space))

legal_actions = env.get_legal_actions()
print("This is the legal action = ", legal_actions)
action = env.action_space.sample(obs["action_mask"])
print("The action value :", action)
new_obs, reward, done, info = env.step(action)

print(new_obs)
env.render(mode = "human")
print("rendered")

# np.random.choice(len(legal_action), 1, p=(legal_action / legal_action.sum()))[0]







#random_action = np.random.choice(len(legal_action), 1, p=(legal_action / legal_action.sum()))[0]
#print(random_action)

#sample one step
# random_action = env.action_space.sample()
# random_action = 0.5
# print(random_action)

# # Step the environment using the sampled action
# new_observation, reward, terminated, truncated, info = env.step(random_action)

# print(new_observation)


