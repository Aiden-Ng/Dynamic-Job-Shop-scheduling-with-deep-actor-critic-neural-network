import gym
import gym.envs
# import gymnasium as gym
import JSSEnv
import os 
import numpy as np
import inspect
from PIL import Image

import plotly.figure_factory as ff
import plotly.io as pio
import imageio
from pathlib import Path
from io import BytesIO

#this is to plot the win rate chart for tardy jobs
import pandas as pd 
from enum import Enum
import argparse
from openpyxl import load_workbook
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Library for actor critic
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_checker import check_env

# Library for PPO
from stable_baselines3 import PPO

# This is for saving the network parameter (weights and biases)
import torch

# To terminate the program
import sys

"""
Things to do
1. Fix the reward function to commodate multi objective
2. Tune the hyperparameters to see the different results

"""

#initialise global variable
images = [] #creates the image for the gif
#for graphing the results
total_jobs = 0
total_number_of_tardy_job = 0

#DEBUG, not sure if can remove this
class action_type(Enum):
    FIFO = 1
    S_RPT = 2
    MTWR = 3
    A2C = 4
    RANDOM = 5

# relative to your local pc
IMG_PATH = (Path(__file__).parent / ".." / "(TESTING) automated_testing" / "(PLOT) makespan").resolve()
GIF_PATH = (Path(__file__).parent / ".." / "(TESTING) automated_testing" / "(GIF) scheduling").resolve()
DEBUG_PATH = (Path(__file__).parent / "(DEBUG)").resolve()

MODEL_VERSION = "A2C_V57" 
TRAINING = False
TIME_STEP = 100000
LOAD_TIME_STEP = 1400000
SAVING_TIME_STEP = 1000000 #timestep for saving

# this is for saving the reinforcement learning models and logging files
models_dir = (Path(__file__).parent / "Model" / f"{MODEL_VERSION}").resolve()
log_dir = (Path(__file__).parent / "model_logs").resolve()
network_param_dir = (Path(__file__).parent / "network_parameters").resolve()

#create argparser object to handle the variables from the automated_test.py
parser = argparse.ArgumentParser(description='Automated test script to run the environment')
parser.add_argument("--episode", help = "specifies the number of episode to run", type = int)
parser.add_argument("--action_type", help = "[action_type.RANDOM, action_type.S_RPT, action_type.MTWR]", type = str)
parser.add_argument("--max_jobs", help = "[25,30,35,40,45,50]", type = int)
parser.add_argument("--logging_xlsx_path", help = "this is the absolute path for the excel file for logging", type = str)
args = parser.parse_args()
args.logging_xlsx_path = (Path(__file__).parent / ".." / "(TESTING) automated_testing" / "automated_test_log.xlsx" ).resolve()

args.episode = 1
args.action_type = "A2C"
args.max_jobs = 30
# args.action_type = "PPO"
# args.action_type = "S_RPT"
# args.action_type = "MTWR"
# args.action_type = "FIFO"
# args.action_type = "RANDOM"

def logging_to_xslx(tardy_ratio_args):
    try:
        wb = load_workbook(args.logging_xlsx_path)
        ws = wb.worksheets[0] #getting the first worksheet
        str_format = "%Y-%m-%d %H:%M:%S"
        Timestamp = datetime.now().strftime(str_format)
        ws.append([Timestamp, 
                   args.episode, 
                   args.action_type, 
                   tardy_ratio_args,
                   str(env.alpha_list), 
                   env.machines, 
                   env.max_jobs, 
                   env.min_proc_time, 
                   env.max_proc_time, 
                   env.operation_num_min, 
                   env.operation_num_max]) #append the data to the worksheet
        wb.save(args.logging_xlsx_path) #save this content
    except Exception as e:
        print(f"Error in {__name__}: {e}") #how do i put the functio nname
        if not ws:
            ws.append([Timestamp,e]) #append the error message to the worksheet
        else:
            print(e)

def saving_to_png():
    plt.figure(figsize=(10,6))
    sns.lineplot(x = "makespan", y = "makespan_count", data = makespan_df, marker='o')
    plt.ylim(0, max(50,0.1*args.episode))
    plt.xlim(0, 1200)
    str_format = "%Y-%m-%d_%H-%M-%S"
    # plt.savefig(f"C:\\Users\\Ng Hong Xi\\OneDrive\\NTU Documents\\Y4S1\\Final Year Project\\Code\\JSSP_Env\\(TESTING) automated_testing\\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_makespan_barplot.png")
    plt.savefig(rf"{IMG_PATH}\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_makespan_barplot.png")

def saving_to_kde():
    plt.figure(figsize=(10,6))
    sns.kdeplot(makespan_df["makespan"], color="blue", label="Dataset 1", fill=True)
    plt.xlabel("Makespan")
    plt.ylabel("Density")
    plt.title("KDE Plot of Makespan Distributions")
    plt.legend()
    str_format = "%Y-%m-%d_%H-%M-%S"
    plt.savefig(rf"{IMG_PATH}\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_makespan_kdeplot.png")

def make_env():
    return gym.make("djss-v1")

main_count = 0
cumulative_reward = 0

if __name__ == "__main__":
    #creating pandas dataframe to store the win rate of tardy jobs
    tardy_df = pd.DataFrame(columns = ["episode","percentage of tardy jobs"])

    #creating data frame for the makespan
    makespan_df = pd.DataFrame(columns = ["makespan", "makespan_count"])

    # EPISODE = args.episode #dyanmic episode
    EPISODE = args.episode
    ACTION_TYPE = args.action_type #changing action_type
    
    #create the environment once
    env = gym.make("djss-v1")
    env.reset(options = {"max_jobs": args.max_jobs}) #this is the max jobs that you want to set
    
    if not TRAINING:
        # model = A2C.load(r"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\rl-baselines3-zoo\rl_zoo3\logs\a2c\djss-v1_1\djss-v1.zip")
        model = A2C.load((models_dir/ f"{LOAD_TIME_STEP}_a2c_djss.zip").resolve(), env = env, verbose =1)

        # loading the network parameters (weights) and biases
        # param = model.get_parameters() #this is to check the parameters of the model
        # torch.save(param, r"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\JSSP_Env\Project\network_parameters\param1.pth")
    
    for episode in range(EPISODE):
        main_count = 0 #reset
        #parallel environment  
        obs, info = env.reset(options = {"max_jobs": args.max_jobs})
        done = False
        # env = DummyVecEnv([make_env for i in range(1)]) # n_envs = 4e
        if ACTION_TYPE == "A2C":
            if TRAINING:
                #check if the folder exists using pathlib
                
                if (models_dir).resolve().exists(): #check if any model exist
                    model = A2C.load((models_dir/ f"{LOAD_TIME_STEP}_a2c_djss.zip").resolve(), env = env, verbose =1, tensorboard_log = log_dir) #this need to do model load
                else:
                    model = A2C("MlpPolicy", env, verbose=1, tensorboard_log = log_dir, ent_coef= 0.01) #this need to do model load    
                    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log = log_dir) #this need to do model load
                    # state_dict = torch.load((network_param_dir / "param1.pth").resolve())
                    # model.set_parameters(state_dict) #load the state dict to the model
                
                #loading the valid weight and biases for the network
                # state_dict = torch.load((network_param_dir / "param1.pth").resolve()) 
                # model.set_parameters(state_dict) #load the state dict to the model    
                for i in range(1,2): 
                #if you want to conitnuously train your model, you have to do reset_num_time_steps = True
                    model.learn(total_timesteps=TIME_STEP, reset_num_timesteps=False, tb_log_name= f"{MODEL_VERSION}")
                    model.save(f"{models_dir}/{LOAD_TIME_STEP + (TIME_STEP * i)}_a2c_djss.zip") #saving the model is the desired directory

                # model.learn(total_timesteps=TIME_STEP, reset_num_timesteps=False, tb_log_name= f"{MODEL_VERSION}")
                # model.save(f"{models_dir}/{SAVING_TIME_STEP}_a2c_djss.zip") #saving the model is the desired directory
                
    
        
        print("=================programme starting=================")
        while not np.all(done):
            # 2. Step the environment
            if ACTION_TYPE == "A2C":
                action, _states = model.predict(obs) 
                
                # log the legal_actions and the action
                with open(DEBUG_PATH / "legal_actions_&_action.txt", "a") as file: #a is append
                    file.write(f"Legal actions: {env.state[:,0][action]}, Selected action: {action}\n")
            
            if ACTION_TYPE != "A2C":
                action = env.get_action(action_type[args.action_type]) #this is the action type that you want to use
                

            obs, reward, done, truncated, info = env.step(action)
            cumulative_reward += reward

            # 3. Render the current schedule as a Plotly figure
            # fig = env.render()  # This returns a Plotly figure.
            # fig.show()
            
            # 4. Convert Plotly figure to an in-memory image
            # try:
            #     img_bytes = pio.to_image(fig, format="png")  # Convert figure to PNG bytes
            #     img = imageio.imread(BytesIO(img_bytes))  # Read image from bytes
            #     images.append(img)  # Store for GIF creation
            #     print(f"Frame {len(images)} added.")
            # except Exception as e:
            #     print("Error converting figure to image:", e)

            main_count += 1
            print(main_count)
            if main_count > 30000:
                makespan_df.to_csv(rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Archive\{args.action_type}_{args.max_jobs}_makespan.csv", header = False , index = False , mode = "a")
                print("exit abruptly")
                #how to reset the value but keep the column
                makespan_df = pd.DataFrame(columns = ["makespan", "makespan_count"])
                break
                
                

            

            if np.all(done): #per epsiode 
                print("End of episode")
                env.time_taken_to_proc_all_jobs = env.total_perform_op_time_jobs + env.total_idle_time_jobs
                number_of_tardy_job = np.sum(env.time_taken_to_proc_all_jobs > env.allowance_jobs)
                total_number_of_tardy_job += number_of_tardy_job
                total_jobs += env.jobs

                #how to insert one row for data frame
                # if env.makespan not in makespan_df["makespan"].values:
                if env.makespan not in makespan_df["makespan"].values:
                    makespan_df.loc[len(makespan_df)] = [env.makespan, 1]
                    makespan_df.sort_values(by = "makespan", ascending = True, inplace = True)
                else: 
                    makespan_df.loc[makespan_df["makespan"] == env.makespan, "makespan_count"] += 1
                
        
        # env.close()

    logging_to_xslx(float(total_number_of_tardy_job)/float(total_jobs)) #open the excel file and write here
    makespan_df.to_csv(rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Archive\{args.action_type}_{args.max_jobs}_makespan.csv", header = False , index = False , mode = "a")
    # saving_to_png()
    saving_to_kde()

    # 5. Save GIF
    # if images:
    #     str_format = "%Y-%m-%d_%H-%M-%S"
    #     gif_path = rf"{GIF_PATH}\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_schedule.gif"
    #     imageio.mimsave(gif_path, images, fps=15)  # Adjust FPS as needed
    #     print(f"GIF saved as {gif_path}!")
    # else:
    #     print("No images were saved. GIF generation failed.")
    
    print("End of programme.")

