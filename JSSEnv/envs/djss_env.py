# dynamic_jss_env.py
import random
import numpy as np
import os
from enum import Enum


if __name__ == "__main__":
    from jss_env1 import JssEnv #if u want to debug from here remove the . from .jss_env1
else:
    from .jss_env1 import JssEnv

from pathlib import Path
from typing import Optional

#this is for manually job arrival
import itertools
import ast #coverts string list "[1,2,3]" to list [1,2,3]

"""
Version : 1.03.0
Date: 10/03/2025

Note:
1. Since the sb3 and openai gym does not really support dynamic action_space, we will be using action_masking with large action_spaces
Future Works:

"""
#this is for the action selection
class action_type(Enum):
    FIFO = 1
    S_RPT = 2
    MTWR = 3
    A2C = 4
    RANDOM = 5

class Debug():
    def __init__(self):
        self.modified_due_date_per_operation = np.array([])
        self.SRPT_ratio = np.array([])
        self.MTWR_ratio = np.array([])
        self.MTWR_max = 0
        self.index = 0

        #debug for file reading
        self.row = 0
        self.job_file = (Path(__file__).parent / ".." / ".." / "Project" / "(DEBUG)" / "dj1.txt").resolve()

class DynamicJssEnv(JssEnv):
    def __init__(self, env_config=None, render_mode=None):
        # Call the static environment’s initializer
        super().__init__(env_config, render_mode)

        #DEBUG initializer
        self.debug = Debug()
        # self.max_proc_time = env_config.get("max_proc_time", 20) 
        
        # Convert the instance_matrix and jobs_length to lists for dynamic appending
        # self.instance_matrix = list(self.instance_matrix) #this is convert the static self.instance_matrix to list
        # self.jobs_length = list(self.jobs_length)
        
        # Initialize dynamic job arrival tracking
        # For already‐loaded jobs, set arrival time to 0 (they’re available immediately)
        
        self.job_arrival_times = {job: 0 for job in range(self.jobs)} #DEBUG, not really usefull because assuming no initial jobs
        self.jobs = len(self.instance_matrix)  # New jobs will have IDs starting from here
        self.alpha_list = [] #this is for the alpha list
        self.alpha = 0 #this sets the job tightness date
        

    def generate_new_job(self):
        #depends if you want dynamic job generation or files
        DYNAMIC_GENERATION = True
        self.jobs += 1 #increment the number of jobs if u added a new job
    
        num_ops = random.randint(self.operation_num_min, self.operation_num_max) #gets random numbers of operation
        machine_order = []
        new_job = []
        total_time = 0
        
        if DYNAMIC_GENERATION:
            #generating the random machining  order for the job, this logic enables no repetition between two conseccutive elements in the list
            while len(machine_order) < num_ops:
                machine_num = np.random.choice(self.machines)
                if len(machine_order) == 0 or machine_order[-1] != machine_num:
                    machine_order.append(machine_num)

            for machine in machine_order:
                time = random.randint(self.min_proc_time, self.max_proc_time) #randomly generate 1 to max_proc_time
                new_job.append((machine, time))
                
                #variables from jssp
                self.max_time_op = max(self.max_time_op, time) #get the maximum time of the operation
                total_time += time #used to get the total time of the job
        
        else: #generating job from a file 
            with open(self.debug.job_file, "r") as instance_file:
                line_str = next(itertools.islice(instance_file, self.jobs -1, None), None)
                new_job = ast.literal_eval(line_str)
                
                for index in range(len(new_job)):
                    self.max_time_op = max(self.max_time_op, new_job[index][1])
                    total_time += new_job[index][1]

        # Append the new job data
        self.instance_matrix.append(new_job)
        self.jobs_length.append(total_time)
        self.max_time_jobs = max(self.jobs_length)
        arrival_time = self.current_time_step  #DEBUG, not sure why this is needed - or add a random delay
        self.job_arrival_times[self.jobs] = arrival_time #DEBUG, not sure why this is needed
        self.jobs_completed = np.append(self.jobs_completed, 0) # this is a boolean to check if the job is completed, so that it will only receive reward once

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
        self.illegal_actions = np.hstack([self.illegal_actions, np.full((self.machines, 1), 0,  dtype=int)])
        # self.state = np.vstack([self.state, np.zeros((1, 7), dtype=float)]) #7 different states

        # ================= PLEASE DEBUG THIS SECTION ================= 
        #add the due date based on proportion of total work (TWK)
        self.alpha_list = [10,20]
        # self.alpha_list = [10,17] #
        self.alpha = random.randint(self.alpha_list[0],self.alpha_list[1]) #this is for 20 jobs
        # self.alpha = random.randint(20,23) #this is for 60 jobs

        due_date =  self.current_time_step + (total_time) * self.alpha
        allowance = (total_time) * self.alpha
        slack = allowance  #total time refers to total processing of the job
        
        self.due_date_jobs = np.append(self.due_date_jobs, due_date)
        self.allowance_jobs = np.append(self.allowance_jobs, allowance) #DEBUG, not sure what this does
        self.flow_time = np.append(self.flow_time, allowance) #this is because self.allowance changes but not flowtime
        self.slack_jobs = np.append(self.slack_jobs, slack) #DEBUG, not sure what this does
        self.allowance_over_slack = self.allowance_jobs / self.slack_jobs #this is to get the ratio of allowance over slack
        # ================= PLEASE DEBUG THIS SECTION =================

        #checking if machine is available, if yes then legal_actions = 1 else legal_actions = 0
        last_index = len(self.instance_matrix) - 1 #used for self.solution
        #check if it is a legal action - must based on the machine needed
        machine_needed = self.instance_matrix[last_index][0][0] #get the machine needed for the job
        if self.machine_legal[machine_needed]: #check if the machine is occupied
            self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 1) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
            self.nb_legal_actions += 1 #increment the number of legal actions, NOT SURE IF THIS IS CORRECT since jss_env is a const val
        else:
            #because machine will be machine_legal = false, to overcome this, we check if the machine is being occupied
            if self.time_until_available_machine[machine_needed] == 0: #check if the machine is available
                self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 1) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
                self.nb_legal_actions += 1 #increment the number of legal actions, NOT SURE IF THIS IS CORRECT since jss_env is a const val
            else:
                self.legal_actions = np.insert(self.legal_actions, len(self.legal_actions)-1, 0) # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
        
        return self.jobs
    
    def get_action(self, action_type_args): #default for random type
        """
        This will follow the S/RPT + SPT dispatching rule to obtain the action

        """

        if action_type_args.value == action_type.FIFO.value:
            action_mask = self.legal_actions
            legal_actions = [i for i, m in enumerate(action_mask) if m == 1]
            action = legal_actions[0]  # naive approach: take the first legal action
            return action

        elif action_type_args.value == action_type.S_RPT.value:   
            if self.legal_actions[:-1].sum() != 0:
                remaining_processing_time = self.jobs_length - self.total_perform_op_time_jobs  #getting the ratio of S/RPT

                SRPT_ratio = np.where( #handles the case when the remaining_processing_time is 0
                    remaining_processing_time == 0,  # Condition: If element is 0
                    np.nan,  # Replace with NaN
                    self.slack_jobs / ((remaining_processing_time) + (remaining_processing_time == 0))  # The remaining_processing_time is 0, then add 1 to avoid division by 0, this is implemented so that the warning does not show
                )

                SRPT_ratio_compare = self.legal_actions[:-1]  #this is becuase we want to clip the SRPT_ratio with 1 so that if SRPT ratio <1 we choose SPT
                
                #get the current processing time at each job's tims step
                #if condition is used to handle when the job is done so that the index does not overflow
                current_processing_time = np.array([
                0 if self.todo_time_step_job[job] == len(self.instance_matrix[job]) #this is to handle the case where the job is done then processing time = 0
                else self.instance_matrix[job][self.todo_time_step_job[job]][1]
                for job in range(len(self.instance_matrix))])

                # ------------------- TEMPORARY DISABLED ------------------- previous
                # no need to do filtering here because the illegal actions will be filtered by modified_due_date_per_operation
                due_date_for_kth_operation =np.where( 
                    self.legal_actions[:-1].astype(bool), #only calculate for legal actions, because it will be wrong for non legal_actions
                    self.total_perform_op_time_jobs + current_processing_time, #get the due date for the kth operation
                    np.nan)
                
                # ------------------- TEMPORARY DISABLED ------------------- incoming
                current_processing_time_filtered =np.where( 
                    self.legal_actions[:-1].astype(bool), #only calculate for legal actions, because it will be wrong for non legal_actions
                    current_processing_time, #get the due date for the kth operation
                    np.nan)
                



                #debug
                SPRT_ratio_current_processing_time = SRPT_ratio * current_processing_time_filtered #get the processing time of the SRPT_ratio_compare
                SRPT_ratio_compare_current_processing_time = SRPT_ratio_compare * current_processing_time_filtered #get the processing time of the SRPT_ratio_compare

                # Use np.where() instead of np.maximum()
                modified_due_date_per_operation = np.where(
                    self.legal_actions[:-1].astype(bool),  # If True (masked), then compute the max, else return np.nan
                    np.maximum(SPRT_ratio_current_processing_time, SRPT_ratio_compare_current_processing_time),  # Compute max only for valid entries
                    np.nan  # Masked values, note that np.nan is a very big value
                )

                index = np.nanargmin(modified_due_date_per_operation)  #get the index of the minimum value
                self.debug.index = index
                return index

            elif self.legal_actions.sum() == 1:
                #to choose NOPE action if no operation are ready for scheduling
                index = np.where(self.legal_actions == 1)[0][0]
                return index
            else:
                assert False, "Error"

        elif action_type_args.value == action_type.MTWR.value:
            if self.legal_actions[:-1].sum() != 0:
                remaining_processing_time = self.jobs_length - self.total_perform_op_time_jobs
                
                MTWR_ratio = np.where(
                                        self.legal_actions[:-1].astype(bool),  # If True (masked), then compute the max, else return np.nan
                                        remaining_processing_time,
                                        np.nan)

                index = np.nanargmax(MTWR_ratio)
                return index
                
            elif self.legal_actions.sum() == 1:
                #to choose NOPE action if no operation are ready for scheduling
                index = np.where(self.legal_actions == 1)[0][0]
                return index
            else:
                assert False, "Error"
        
        elif action_type_args.value == action_type.RANDOM.value:
            index = np.random.choice(len(self.legal_actions), 1, p=(self.legal_actions / self.legal_actions.sum()) )[0] #how is it possible to take NOACTION
            return index


    def step(self, action: int, **kwargs): #kwargs used to overwrite the action
        # With 10% probability, generate a new job.
        # if random.random() < 1: #make it generate new job for everystep
        
        truncated = None #this required for the gym environment

        # how to set a probability of <0.4, make this such that new job arrival would not come in certain timestep
        if random.random() < 0.2:
            if (len(self.instance_matrix) < self.max_jobs): 
                for i in range(10):
                    new_job = self.generate_new_job()
                    self._get_current_state_representation() #this is to update the current state representation to accomodate new job arrivals
                    #for every new job that comes, we have to update the state

                    #if self.job_arrival_times[new_job] <= self.current_time_step: #DEBUG, not sure what this does
                        #self.legal_actions[new_job] = 1 #DEBUG, not sure what this does
                    if (len(self.instance_matrix) >= self.max_jobs): 
                        break

        #if take illegal actions
        if __name__ != "__main__": #if agent make decision
        #check if it is illegal action
            if self.state[:, 0][action] != 1 : #DEBUG, need to handle NOPE action
                reward = -1
                return (self._get_current_state_representation(),
                        reward,
                        self._is_done(),
                        truncated,
                        {}
                )
        
        # if not kwargs:
        #     action = self.get_action(action_type[action])
        # else:
        #     for key , value in kwargs.items():
        #         if key == "action":
        #             action = value
        #             break

        obs, reward, done, info = super().step(action)
        return obs, reward, done, truncated, info
    
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        #note that seed is not used
        
        obs, info = super().reset(callback=self.generate_new_job, env_config=options)  # generate new job after resets
        
        # return obs, info
        return obs, info #info is not included, because VecEnv only returns obs 

if __name__ == '__main__':
    env = DynamicJssEnv()
    for episode in range(10):
        #obs, info = env.reset(callback = env.generate_new_job) #generate new job after reset
        obs, info = env.reset() #generate new job after reset
        done = False
        cum_reward = 0
        while not done:
            # legal_actions = obs["action_mask"]
            # p = (legal_actions / legal_actions.sum()) #legal action got problem
            # actions = np.random.choice(len(legal_actions), 1, p=(legal_actions / legal_actions.sum()) )[0] #how is it possible to take NOACTION
            
            obs, rewards, done, _, info = env.step("S_RPT") #this goes to the step function inside the djss_env, not the jsse_env
            cum_reward += rewards
        print(f"Cumulative reward: {cum_reward}")

        #loggint the number of tardy jobs 
               

