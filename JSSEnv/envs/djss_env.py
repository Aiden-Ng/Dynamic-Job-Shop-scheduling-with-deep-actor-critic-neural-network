# dynamic_jss_env.py
import random
import numpy as np
import os
print(os.getcwd())
from .jss_env import JssEnv



class DynamicJssEnv(JssEnv):
    def __init__(self, env_config=None, render_mode=None):
        # Call the static environment’s initializer
        super().__init__(env_config, render_mode)
        # self.max_proc_time = env_config.get("max_proc_time", 20) 
        
        # Convert the instance_matrix and jobs_length to lists for dynamic appending
        # self.instance_matrix = list(self.instance_matrix) #this is convert the static self.instance_matrix to list
        # self.jobs_length = list(self.jobs_length)
        
        # Initialize dynamic job arrival tracking
        # For already‐loaded jobs, set arrival time to 0 (they’re available immediately)
        
        self.job_arrival_times = {job: 0 for job in range(self.jobs)} #DEBUG, not really usefull because assuming no initial jobs
        self.jobs = len(self.instance_matrix)  # New jobs will have IDs starting from here

    def generate_new_job(self):
        self.jobs += 1 #increment the number of jobs if u added a new job
        
        #check if the number of job is full
        if len(self.instance_matrix) < self.jobs: #note instance_matrix is a 2D array with tuple
            num_ops = random.randint(self.operation_num_min, self.operation_num_max) #gets random numbers of operation
            machine_order = []
            new_job = []
            total_time = 0

            #generating the random machining  order for the job, this logic enables no repetition between two conseccutive elements in the list
            while len(machine_order) < num_ops:
                machine_num = np.random.choice(self.machines)
                if len(machine_order) == 0 or machine_order[-1] != machine_num:
                    machine_order.append(machine_num)

            for machine in machine_order:
                time = random.randint(1, self.max_proc_time) #randomly generate 1 to max_proc_time
                new_job.append((machine, time))
                
                #variables from jssp
                self.max_time_op = max(self.max_time_op, time) #get the maximum time of the operation
                total_time += time #used to get the total time of the job

            # Append the new job data
            self.instance_matrix.append(new_job)
            self.jobs_length.append(total_time)
            self.max_time_jobs = max(self.jobs_length)
            arrival_time = self.current_time_step  #DEBUG, not sure why this is needed - or add a random delay
            self.job_arrival_times[self.jobs] = arrival_time #DEBUG, not sure why this is needed

            self.sum_op += total_time #get the total time of operation of all jobs

            # Expand the required arrays for dynamic job arrival
            self.legal_actions = np.append(self.legal_actions, 0) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
            self.solution = np.vstack([self.solution, np.full((1, self.machines), -1,  dtype=int)]) #add a new row to the solution matrix
            self.time_until_finish_current_op_jobs = np.append(self.time_until_finish_current_op_jobs, 0)
            self.todo_time_step_jobs = np.append(self.todo_time_step_jobs, 0)
            self.total_perform_op_time_jobs = np.append(self.total_perform_op_time_jobs, 0)
            self.needed_machine_jobs = np.append(self.needed_machine_jobs, 0)
            self.total_idle_time_jobs = np.append(self.total_idle_time_jobs, 0)
            self.idle_time_jobs_last_op = np.append(self.idle_time_jobs_last_op, 0)
            self.action_illegal_no_op = np.append(self.action_illegal_no_op, 0)








            return self.jobs
    
    """ORIGINAL GENERATE_NEW_JOB FUNCTION
    def generate_new_job(self):
        new_job_id = self.next_job_id #not sure if need 
        self.next_job_id += 1         #not sure if need 

        num_ops = self.machines
        machine_order = np.random.permutation(self.machines)
        new_job = []
        total_time = 0
        for op in range(num_ops):
            machine = int(machine_order[op])
            proc_time = random.randint(1, self.max_proc_time)
            new_job.append((machine, proc_time))
            total_time += proc_time

        # Append the new job data
        self.instance_matrix.append(new_job)
        self.jobs_length.append(total_time)
        arrival_time = self.current_time_step  # or add a random delay
        self.job_arrival_times[new_job_id] = arrival_time

        # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
        self.legal_actions = np.append(self.legal_actions, 0)

        return new_job_id
    """
    
    def step(self, action: int):
        # With 10% probability, generate a new job.
        if random.random() < 1: #make it generate new job for everystep
            new_job = self.generate_new_job()
            if self.job_arrival_times[new_job] <= self.current_time_step:
                self.legal_actions[new_job] = 1

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info

if __name__ == '__main__':
    env = DynamicJssEnv()
    obs = env.reset()
    env.generate_new_job() #generate new job after reset
    done = False
    cum_reward = 0
    while not done:
        legal_actions = obs["action_mask"]
        actions = np.random.choice(
            len(legal_actions), 1, p=(legal_actions / legal_actions.sum())
        )[0]
        obs, rewards, done, _ = env.step(actions)
        cum_reward += rewards
    print(f"Cumulative reward: {cum_reward}")