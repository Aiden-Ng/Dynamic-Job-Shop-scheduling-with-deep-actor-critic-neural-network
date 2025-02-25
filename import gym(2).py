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

INSTANCE_PATH = r"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\JSSEnv\envs\instances\ta01"
print(os.getcwd())
env = gym.make('jss-v1',  env_config={'instance_path': INSTANCE_PATH})
print(gym.envs.registry.keys())
obs, info = env.reset()
done = False

images = []

print("=================programme starting=================")
while not done:
    # 1. Choose an action (random, or from a policy). Here we pick the first legal action as a demo:
    print("=================programme starting=================")
    action_mask = obs["action_mask"]
    legal_actions = [i for i, m in enumerate(action_mask) if m == 1]
    action = legal_actions[0]  # naive approach: take the first legal action
    print("=================programme starting=================")
    # 2. Step the environment
    obs, reward, done, info = env.step(action)

    # 3. Render the current schedule as a Plotly figure
    fig = env.render()  # This returns a Plotly figure.
    fig.show()
    print(type(fig))  # Ensure it's a valid Plotly figure
    print(env.instance_matrix)

#     # 4. Convert Plotly figure to an in-memory image
#     try:
#         img_bytes = pio.to_image(fig, format="png")  # Convert figure to PNG bytes
#         img = imageio.imread(BytesIO(img_bytes))  # Read image from bytes
#         images.append(img)  # Store for GIF creation
#         print(f"Frame {len(images)} added.")
#     except Exception as e:
#         print("Error converting figure to image:", e)

# env.close()

# # 5. Save GIF
# if images:
#     gif_path = r"C:\Users\Ng Hong Xi\OneDrive\NTU Documents\Y4S1\Final Year Project\Code\JSSP_Env\schedule.gif"
#     imageio.mimsave(gif_path, images, fps=2)  # Adjust FPS as needed
#     print(f"GIF saved as {gif_path}!")
# else:
#     print("No images were saved. GIF generation failed.")

print("End of programme.")

#dynamic scheduling's main
# import numpy as np
# from dynamic_jss_env import DynamicJssEnv

# env_config = {"instance_path": "path/to/your/dynamic_instance.txt"}
# env = DynamicJssEnv(env_config=env_config)
# obs, info = env.reset()
# done = False

# while not done:
#     legal_actions = obs["action_mask"]
#     valid_actions = np.flatnonzero(legal_actions)
#     action = np.random.choice(valid_actions)
#     obs, reward, done, info = env.step(action)
#     print("Reward:", reward)