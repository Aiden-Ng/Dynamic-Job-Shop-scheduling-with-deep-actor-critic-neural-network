import numpy as np
import random


# Initialize global variables
instance_matrix = []
jobs = 5
operation_num_min = 5
operation_num_max = 15
machines = 10
max_proc_time = 10
max_time_op = 0
jobs_length = []
current_time_step = 0
job_arrival_times = {}
sum_op = 0
legal_actions = np.array([])

for i in range(2):
    if len(instance_matrix) < jobs:  # note instance_matrix is a 2D array with tuple
        num_ops = random.randint(operation_num_min, operation_num_max)  # gets random numbers of operation
        machine_order = []
        new_job = []
        total_time = 0

        # generating the random machining order for the job, this logic enables no repetition between two consecutive elements in the list
        while len(machine_order) < num_ops:
            machine_num = np.random.choice(machines)
            if len(machine_order) == 0 or machine_order[-1] != machine_num:
                machine_order.append(machine_num)

        for machine in machine_order:
            time = random.randint(1, max_proc_time)  # randomly generate 1 to max_proc_time
            new_job.append((machine, time))

            # variables from jssp
            max_time_op = max(max_time_op, time)  # get the maximum time of the operation
            total_time += time  # used to get the total time of the job

        # Append the new job data
        instance_matrix.append(new_job)
        jobs_length.append(total_time)
        max_time_jobs = max(jobs_length)
        arrival_time = current_time_step  # or add a random delay
        job_arrival_times[len(job_arrival_times)] = arrival_time

        sum_op += total_time  # get the total time of operation of all jobs

        # Expand legal_actions (Gym action_space is normally fixed, so here we dynamically extend it)
        legal_actions = np.append(legal_actions, 0)

        new_job_id = len(job_arrival_times) - 1
