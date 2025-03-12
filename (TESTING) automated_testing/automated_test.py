import subprocess
import argparse
from enum import Enum
from datetime import datetime
import os
from pathlib import Path
"""
Version 1.0.0
1. This is the automated test script to run the environment
"""
#how to get the files working directory
RL_environment_dir = (Path(__file__).parent / "..").resolve()
RL_environment_ABS_FILE_PATH = f"{RL_environment_dir}\\RL_environment.py"

class action_type(Enum):
    FIFO = 1
    S_RPT = 2
    MWTR = 3

#creating the parser object
EPISODE_LIST = [500,1000,3000]
ACTION_TYPE_LIST = [action_type.FIFO, action_type.S_RPT, action_type.MWTR]

def call_test(episode_args, action_type_args = None):
    try:
        #running the RL_environment.py path
        subprocess.run(f"python \"{RL_environment_ABS_FILE_PATH}\" --episode {episode_args} --action_type {action_type_args.name}", shell=True) #it will be running here
        print(f"config [epsiode,action_type] : [{episode_args},{action_type_args}]")

    except Exception as e:
        print("Error",e) #idk what to expect

if __name__ == '__main__':
    for episode in EPISODE_LIST:
        # for action_type in action_enum:
        for action in ACTION_TYPE_LIST:
         call_test(episode, action)
         
            
        
