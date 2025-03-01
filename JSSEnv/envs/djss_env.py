# dynamic_jss_env.py
import random
import numpy as np
import os
from .jss_env1 import JssEnv #if u want to debug from here remove the . from .jss_env1

"""
Version : 1.01
Date: 1/3/2025

Note:
1. This is a wrapper for jss_env1.py to handle dynamic job arrival
2. jss_env1.py modified from jss_env to accomodate dynamic jobs
3. Stable DJssEnv able to handle dynamic job arrival for only 2 machine

Future Works:
1. Able to pop the job once it done and align the index
2. make rendering work
"""

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
        self.max_jobs = 100 #set the max number of jobs allowable

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

            # this affect the legal actions
            last_index = len(self.instance_matrix) - 1 #used for self.solution
            self.solution.append(np.full((len(self.instance_matrix[last_index])), -1,  dtype=int)) #add a new row to the solution matrix
            self.time_until_finish_current_op_jobs = np.append(self.time_until_finish_current_op_jobs, 0) #DEBUG, not sure if needs to be updated
            self.todo_time_step_job = np.append(self.todo_time_step_job, 0) #correct cuz its 0
            self.total_perform_op_time_jobs = np.append(self.total_perform_op_time_jobs, 0) #DEBUG, unsure what is this
            self.needed_machine_jobs = np.append(self.needed_machine_jobs, self.instance_matrix[last_index][0][0]) #DEBUG, append then update the needed machine
            self.total_idle_time_jobs = np.append(self.total_idle_time_jobs, 0)
            self.idle_time_jobs_last_op = np.append(self.idle_time_jobs_last_op, 0)
            self.action_illegal_no_op = np.append(self.action_illegal_no_op, 0)
            self.illegal_actions = np.hstack([self.illegal_actions, np.full((self.machines, 1), -1,  dtype=int)])
            self.state = np.vstack([self.state, np.full((1, 7), -1,  dtype=int)]) #7 different states

            # ============ DEBUG HERE ============ soemthing wrong with this logic CANNOT
            last_index = len(self.instance_matrix) - 1 #used for self.solution
            #check if it is a legal action - must based on the machine needed
            machine_needed = self.instance_matrix[last_index][0][0] #get the machine needed for the job
            if self.machine_legal[machine_needed]: #check if the machine is occupied
                self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 1) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
                self.nb_legal_actions += 1 #increment the number of legal actions, NOT SURE IF THIS IS CORRECT since jss_env is a const val
            else:
                #because init machine will be machine_legal = false, to overcome this, we check if the machine is being occupied
                if self.time_until_available_machine[machine_needed] == 0: #check if the machine is available
                    self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 1) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
                    self.nb_legal_actions += 1 #increment the number of legal actions, NOT SURE IF THIS IS CORRECT since jss_env is a const val
                else:
                    self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 0) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
            
            return self.jobs
    
    def step(self, action: int):
        # With 10% probability, generate a new job.
        # if random.random() < 1: #make it generate new job for everystep
        if (len(self.instance_matrix) < self.max_jobs): 
            new_job = self.generate_new_job()
            if self.job_arrival_times[new_job] <= self.current_time_step: #DEBUG, not sure what this does
                self.legal_actions[new_job] = 1 #DEBUG, not sure what this does

        obs, reward, done, info = super().step(action)
        return obs, reward, done, info

if __name__ == '__main__':
    for i in range(10000):
        print(i)
        env = DynamicJssEnv()
        #obs, info = env.reset(callback = env.generate_new_job) #generate new job after reset
        obs, info = env.reset(callback = env.generate_new_job) #generate new job after reset
        done = False
        cum_reward = 0
        while not done:
            legal_actions = obs["action_mask"]
            p = (legal_actions / legal_actions.sum()) #legal action got problem
            actions = np.random.choice(len(legal_actions), 1, p=(legal_actions / legal_actions.sum()) )[0] #how is it possible to take NOACTION
            obs, rewards, done, _ = env.step(actions) #this goes to the step function inside the djss_env, not the jsse_env
            cum_reward += rewards
        print(f"Cumulative reward: {cum_reward}")
        del env