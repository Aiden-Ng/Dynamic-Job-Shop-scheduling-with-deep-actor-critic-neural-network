import rl_zoo3
import pathlib as Path
import subprocess
import argparse

#how to check if the package exist

#assuming you have list of variables - start
ALGO_VERSION = "A2C_V3"
TRAIN_PY = rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\rl-baselines3-zoo\train.py"
MODEL_PATH = rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\JSSP_Env\Project\Model\{ALGO_VERSION}"
TENSOR_BOARD_PATH = rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\JSSP_Env\Project\model_logs\{ALGO_VERSION}"
LOG = rf"D:\NTU document\Academic stuff (NTU)\Y4S1\Final Year Project\Code\JSSP_Env\Project\logs"
#assuming you have list of variables - end


#creating the arg parser object - start
"""
-i <- TRAINED_AGENT, path to a pretrained agent to continue
-n <- N_TIMESTEPS, overwrite the number of timesteps
-tb <- TENSORBOARD_LOG, Tensorboard log dir
-optimize <- OPTIMIZE, run hyperparameters search
--eval-freq <- EVAL_FREQ, overwrite the evaluation frequency NOT SURE WHAT IS THIS
--optimization-log-path <- OPTIMIZATION_LOG_PATH, Path to save the log and optimal policy for each hyperparameter tried during optimization
-f <- LOG_FOLDER,
"""

parser = argparse.ArgumentParser(description='Automated test script to run the environment')
parser.add_arguments("--algo", help = "type of algorithm", type = str)
parser.add_arguments("--trained_model_path", help = "trained agent", type = str)
parser.add_arguments("--n_timesteps", help = "number of timesteps", type = int)
parser.add_arguments("--env", help = "the environment", type = str)
parser.add_arguments("--tensor_board_path", help = "provides the tensorboard logging path", type = str)
parser.add_arguments("--optimize", help = "the environment", type = bool)
parser.add_arguments("--model_path", help = "path to save the model", type = str)
parser.add_arguments("--log_folder", help = "path to save the log", type = str)
args = parser.parse_args()

# setting the values manually before yaml implementation
args.algo = "a2c"
args.env = "djss-v1" #this is the id that you registered to GYM
args.optimize = "False" #this is the default value
args.tensor_board_path = TENSOR_BOARD_PATH
args.model_path = MODEL_PATH #path to a pretrained agent
args.log_folder = LOG

#creating the arg parser object - end
def call_test():
    try:
        subprocess.run(rf"python \"{TRAIN_PY}\" --algo {args.algo} --env {args.env} -optimize {args.optimize} -tb {TENSOR_BOARD_PATH}",shell = True)  
    except Exception as e:
        print("Error",e)
    


def main():
    call_test()

main()

