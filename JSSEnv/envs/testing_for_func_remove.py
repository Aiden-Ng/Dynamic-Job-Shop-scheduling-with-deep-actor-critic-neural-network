import numpy as np
import random

class testEnv:
    def __init__(self):
        self.machines = 20
        self.instance_matrix = None

    def _generate_random_job(self):
        """
        Returns a list of (machine, time) pairs representing the routing for a new job.
        For example, each job must visit each machine once in a random order,
        or you can define something else.
        """
        # Suppose each new job must go through 'self.machines' operations in random order:
    
        machine = random.randint(0, self.machines-1)
        # can u make a normal distribution for job ranges from 0 - 100
        values = np.arange(101)  # Discrete range [0, 100]
        # Define normal-like probability distribution
        mean = 50  # Center of distribution
        std_dev = 15  # Spread of distribution
        # Compute probability weights using the normal distribution formula
        probs = np.exp(-((values - mean) ** 2) / (2 * std_dev**2))
        probs /= probs.sum()  # Normalize to sum to 1

        # Sample from the discrete range following normal-like distribution
        time = np.random.choice(values, size=1, p=probs)[0]
        self.instance_matrix = (machine, time)
        print(self.instance_matrix)
        return 
    
env = testEnv()
env._generate_random_job()