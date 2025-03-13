import gym
import gym.envs
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

#create argparser object to handle the variables from the automated_test.py
parser = argparse.ArgumentParser(description='Automated test script to run the environment')
parser.add_argument("--episode", help = "specifies the number of episode to run", type = int)
parser.add_argument("--action_type", help = "[action_type.RANDOM, action_type.S_RPT, action_type.MTWR]", type = str)
parser.add_argument("--logging_xlsx_path", help = "this is the absolute path for the excel file for logging", type = str)
args = parser.parse_args()
args.logging_xlsx_path = (Path(__file__).parent / "(TESTING) automated_testing" / "automated_test_log.xlsx" ).resolve()
# args.episode = 1
# args.action_type = "S_RPT"
# args.action_type = "MTWR"
# args.action_type = "FIFO"

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
    plt.savefig(rf"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\(TESTING) automated_testing\(PLOT) makespan\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_makespan_barplot.png")

def saving_to_kde():
    plt.figure(figsize=(10,6))
    sns.kdeplot(makespan_df["makespan"], color="blue", label="Dataset 1", fill=True)
    plt.xlabel("Makespan")
    plt.ylabel("Density")
    plt.title("KDE Plot of Makespan Distributions")
    plt.legend()
    str_format = "%Y-%m-%d_%H-%M-%S"
    plt.savefig(rf"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\(TESTING) automated_testing\(PLOT) makespan\{datetime.now().strftime(str_format)}_{args.action_type}_{args.episode}_makespan_kdeplot.png")


if __name__ == "__main__":
    #creating pandas dataframe to store the win rate of tardy jobs
    tardy_df = pd.DataFrame(columns = ["episode","percentage of tardy jobs"])

    #creating data frame for the makespan
    makespan_df = pd.DataFrame(columns = ["makespan", "makespan_count"])

    # EPISODE = args.episode #dyanmic episode
    EPISODE = args.episode
    ACTION_TYPE = args.action_type #changing action_type

    for episode in range(EPISODE):
        env = gym.make('djss-v1')
        obs, info = env.reset(callback = env.generate_new_job)
        done = False
        print("=================programme starting=================")
        while not done:
            # 1. Choose an action (random, or from a policy). Here we pick the first legal action as a demo:
            print("=================programme starting=================")
            # action_mask = obs["action_mask"]
            # legal_actions = [i for i, m in enumerate(action_mask) if m == 1]
            # action = legal_actions[0]  # naive approach: take the first legal action
            print("=================programme starting=================")
            # 2. Step the environment
            obs, reward, done, info = env.step(args.action_type)

            # 3. Render the current schedule as a Plotly figure
            # fig = env.render()  # This returns a Plotly figure.
            # fig.show()
            # print(type(fig))  # Ensure it's a valid Plotly figure
            print(env.instance_matrix)

            # # 4. Convert Plotly figure to an in-memory image
            # try:
            #     img_bytes = pio.to_image(fig, format="png")  # Convert figure to PNG bytes
            #     img = imageio.imread(BytesIO(img_bytes))  # Read image from bytes
            #     images.append(img)  # Store for GIF creation
            #     print(f"Frame {len(images)} added.")
            # except Exception as e:
            #     print("Error converting figure to image:", e)

            if done: #per epsiode 
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
                
        
        env.close()

    logging_to_xslx(float(total_number_of_tardy_job)/float(total_jobs)) #open the excel file and write here
    # saving_to_png()
    saving_to_kde()

    # # 5. Save GIF
    # if images:
    #     gif_path = rf"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\{args.action_type}_schedule.gif"
    #     imageio.mimsave(gif_path, images, fps=15)  # Adjust FPS as needed
    #     print(f"GIF saved as {gif_path}!")
    # else:
    #     print("No images were saved. GIF generation failed.")

    print("End of programme.")

