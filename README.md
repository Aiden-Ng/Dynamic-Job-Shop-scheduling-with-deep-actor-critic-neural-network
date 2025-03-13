# Final Year Project - Dynamic Job-Shop Scheduling Environment 

An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

![til](./tests/ta01.gif)

Getting Started
------------


How To Use
------------

The observation provided by the environment contains both a boolean array indicating if the action is legal or not and the "real" observation

```python 
self.observation_space = gym.spaces.Dict({
            "action_mask": gym.spaces.Box(0, 1, shape=(self.jobs + 1,)),
            "real_obs": gym.spaces.Box(low=0.0, high=1.0, shape=(self.jobs, 7), dtype=np.float),
        })
```

A random agent would have to sample legal action from this `action_mask` array, otherwise, you might take illegal actions.  
In theory, it is not possible to take the same action over and over again as the job will have one of his operations currently on a machine and might not be free for schedule.  

For research purposes, I've made a random loop using RLLib: https://github.com/prosysscience/RL-Job-Shop-Scheduling/blob/0bbe0c0f2b8a742b75cbe67c5f6a825b8cfdf5eb/JSS/randomLoop/random_loop.py

If you don't want to use RLLib, you can write a simple random loop using `numpy.random.choice` function:

```python
import numpy as np
np.random.choice(len(legal_action), 1, p=(legal_action / legal_action.sum()))[0]
```

Where `legal_action` is the array of legal action (i.e., `action_mask`).  
This line of code will randomly sample one legal action from the `action_mask`.

Project Organization
------------

    ├── README.md             <- The top-level README for developers using this project.
    ├── JSSEnv
    │   └── envs              <- Contains the environment.
    │       └── instances     <- Contains some intances from the litterature.
    │
    └── tests                 
        │
        ├── test_state.py     <- Unit tests focus on testing the state produced by
        │                        the environment.
        │
        ├── test_rendering.py <- Unit tests for the rendering, mainly used as an example
        |                        how to render the environment.
        │
        └── test_solutions.py <- Unit tests to ensure that our environment is correct checking
                                 known solution in the litterature leads to the intended make-
                                 span. We also check if all actions provided by the solution are
                                 legal in our environment.
--------


## License

MIT License
