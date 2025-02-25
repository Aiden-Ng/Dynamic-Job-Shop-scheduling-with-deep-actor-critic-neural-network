import numpy as np
import random

# Step 1: Initialize an empty NumPy array with shape (0,2)
job_id = 0
machine = 15 #number of machines
machines = list(range(machine))
max_proc_time = 99
jobs = 15


# Start with an empty array to store (Machine, Time) pairs
instance_matrix = [] #this is for all the operation_array_episode
jobs_length = []

for i in range(3):
    operation_array_episode = []
    operation_num = random.randint(5, 15)  # Generate a random number of operations (between 5 and 15)
    jobs_length.append(0) #create a new length space to store the jobs length
    job_nb = len(instance_matrix) #get the current job number
    for _ in range(operation_num):
        machine_num = random.choice(machines)  # Select a machine randomly
        time = random.randint(1, max_proc_time)  # Generate a random processing time
        operation_array_episode.append([machine_num, time])

        #keep all the dynamic job times into the job length
        jobs_length[job_nb] += time

    operation_array_episode = np.array(operation_array_episode)
    instance_matrix.append(operation_array_episode)

# Step 3: Print final result


if __name__ == "__main__":
    print(random.randint(0, jobs -1))
    machines = 10
    num_ops = 5
    machine_order = []
    while len(machine_order) < num_ops:
        machine_num = np.random.choice(machines)
        if len(machine_order) == 0 or machine_order[-1] != machine_num:
            machine_order.append(machine_num)
    
    print(type(machine_order))
    