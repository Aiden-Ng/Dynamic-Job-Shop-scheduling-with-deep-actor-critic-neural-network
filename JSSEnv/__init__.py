from gym.envs.registration import register

register(
    id="jss-v1",
    entry_point="JSSEnv.envs:JssEnv",
)


register(
    id="djss-v1",
    entry_point="JSSEnv.envs:DynamicJssEnv",
)


