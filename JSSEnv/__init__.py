from gym.envs.registration import register
from gymnasium.envs.registration import register as gymnasium_register #this is for rl_zoo3 since it uses gymnaisum

register(
    id="jss-v1",
    entry_point="JSSEnv.envs:JssEnv",
)


register(
    id="djss-v1",
    entry_point="JSSEnv.envs:DynamicJssEnv",
)

#this registers for the newer gym
gymnasium_register(
    id="djss-v1",
    entry_point="JSSEnv.envs:DynamicJssEnv",
)