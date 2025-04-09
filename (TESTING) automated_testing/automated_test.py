import subprocess
import argparse
from enum import Enum
from datetime import datetime
import os
from pathlib import Path

#how to get the files working directory
RL_environment_ABS_FILE_PATH = (Path(__file__).parent / ".." / "RL_environment.py").resolve()

class action_type(Enum):
    FIFO = 1
    S_RPT = 2
    MTWR = 3
    A2C = 4
    RANDOM = 5


#creating the parser object
# EPISODE_LIST = 50
EPISODE_LIST = [3000]

# ACTION_TYPE_LIST = [action_type.A2C]
ACTION_TYPE_LIST = [action_type.RANDOM]

MAX_JOBS_LIST = [25,30,35,40]
# MAX_JOBS_LIST = [40]

def call_test(episode_args, action_type_args, max_jobs_args):
    try:
        #running the RL_environment.py path
        subprocess.run(f"python \"{RL_environment_ABS_FILE_PATH}\" --episode {episode_args} --action_type {action_type_args.name} --max_jobs {max_jobs_args}", shell=True) #it will be running here
        print(f"config [epsiode,action_type] : [{episode_args},{action_type_args}]")

    except Exception as e:
        print("Error",e) #idk what to expect

if __name__ == '__main__':
    for action in ACTION_TYPE_LIST:
        for episode in EPISODE_LIST:
            for max_jobs in MAX_JOBS_LIST:
                call_test(episode, action, max_jobs)
         
            
        
