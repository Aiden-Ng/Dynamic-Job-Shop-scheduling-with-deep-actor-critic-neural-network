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

INSTANCE_PATH = r"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\JSSEnv\envs\instances\ta01"
print(os.getcwd())

images = []

#for graphing the results
total_jobs = 0
total_number_of_tardy_job = 0


#creating pandas dataframe to store the win rate of tardy jobs
results_df = pd.DataFrame(columns = ["episode","percentage of tardy jobs"])
EPISODE = 100
for episode in range(EPISODE):
    env = gym.make('djss-v1',  env_config={'instance_path': INSTANCE_PATH})
    obs, info = env.reset(callback = env.generate_new_job)
    done = False
    print("=================programme starting=================")
    while not done:
        # 1. Choose an action (random, or from a policy). Here we pick the first legal action as a demo:
        print("=================programme starting=================")
        # action_mask = obs["action_mask"]
        # legal_actions = [i for i, m in enumerate(action_mask) if m == 1]
        # action = legal_actions[0]  # naive approach: take the first legal action
        action = env.get_action()

        print("=================programme starting=================")
        # 2. Step the environment
        obs, reward, done, info = env.step(action)

        # 3. Render the current schedule as a Plotly figure
        fig = env.render()  # This returns a Plotly figure.
        # fig.show()
        print(type(fig))  # Ensure it's a valid Plotly figure
        print(env.instance_matrix)

        # 4. Convert Plotly figure to an in-memory image
        try:
            img_bytes = pio.to_image(fig, format="png")  # Convert figure to PNG bytes
            img = imageio.imread(BytesIO(img_bytes))  # Read image from bytes
            images.append(img)  # Store for GIF creation
            print(f"Frame {len(images)} added.")
        except Exception as e:
            print("Error converting figure to image:", e)

        if done: #per epsiode
            
            env.time_taken_to_proc_all_jobs = env.total_perform_op_time_jobs + env.total_idle_time_jobs
            number_of_tardy_job = np.sum(env.time_taken_to_proc_all_jobs > env.allowance_jobs)
            total_number_of_tardy_job += number_of_tardy_job
            total_jobs += env.jobs

    
    env.close()

results_df.loc[0] = [EPISODE, float(float(total_number_of_tardy_job)/float(total_jobs))]
print(results_df)


# 5. Save GIF
if images:
    gif_path = r"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\schedule.gif"
    imageio.mimsave(gif_path, images, fps=15)  # Adjust FPS as needed
    print(f"GIF saved as {gif_path}!")
else:
    print("No images were saved. GIF generation failed.")

print("End of programme.")

