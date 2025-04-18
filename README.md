## Table of Contents

- [Dynamic Job Shop Scheduling (DJSSP) environment configuration](#dynamic-job-shop-scheduling-djssp-environment-configuration)
- [Dispatching Rule](#dispatching-rule)
  - [Gif (Just demonstration for each dispatching rule)](#gif-just-demonstration-for-each-dispatching-rule)
  - [Example of each scheduling method per EPISODE](#example-of-each-scheduling-method-per-episode)
- [Deep reinforcement learning actor-critic (Stable baseline 3 + OpenAI Gym)](#deep-reinforcement-learning-actor-critic-stable-baseline-3--openai-gym)
  - [Reward Function design (Dense reward function)](#reward-function-design-dense-reward-function)
  - [Synchronous actor critic reinforcement learning (A2C from stable baseline 3)](#synchronous-actor-critic-reinforcement-learning-a2c-from-stable-baseline-3)
  - [Multi - layer perceptron configurations (MLP - policy from stable baseline 3)](#multi---layer-perceptron-configurations-mlp---policy-from-stable-baseline-3)
  - [Deep actor-critic reinforcement learning results](#deep-actor-critic-reinforcement-learning-results)
  - [Comparing both Dispatching rule and Deep actor-critic reinforcement learning](#comparing-both-dispatching-rule-and-deep-actor-critic-reinforcement-learning)
    - [Tardy jobs comparison](#tardy-jobs-comparison)
    - [Makespan comparison, the makespan KDE plot is calculated from simulations with 5000 episodes.](#makespan-comparison-the-makespan-kde-plot-is-calculated-from-simulations-with-5000-episodes)
- [YET TO DO](#yet-to-do)
- [Project Organization](#project-organization)
- [License](#license)





### Gif (Just demonstration for each dispatching rule)

# Final Year Project - Dynamic Job-Shop Scheduling Environment 
An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

## Abstract
------------
This repository contains all the code for the implementation of deep actor-critic reinforcement learning for dynamic job shop scheduling problem (DJSSP). The open sources libraries that was used for this implementation includes Stable Baseline 3 for the deep actor critic reinforcement learning and Open AI Gym for the DJSSP implementation.

## Example of each scheduling method per EPISODE
1. First in first out (FIFO)

 ![GIF not loaded](./(GITHUB)%20Graphs/result_FIFO_schedule.gif)

2. S/RPT + SPT (Job Slack/Remaining Processing Time) combined with Shortest Processing Time

 ![GIF not loaded](./(GITHUB)%20Graphs/result_S_RPT_schedule.gif)

3. Most Total Work Remaining (MTWR)

 ![GIF not loaded](./(GITHUB)%20Graphs/result_MWTR_schedule.gif)

## Dynamic Job Shop Scheduling (DJSSP) environment configuration
------------
The dynamic job scheduling environment is characteristed by these parameters: 
- **Number of Machines**: `6`
- **Maximum Allowable Jobs**: `25` to `40` with intervals of 5
- **Processing Time Range**: `[50, 60]`
- **Allowable Number of Operations per Job**: `[8, 9]`
- **Due Date Tightness (α)**: `[10, 20]`
The variation between each variable are kept minimum to allow for a more stable result. 

## Dispatching Rule
------------
S_RPT + SPT is chosen because of its ability to reduce number of job tardiness. MTWR is chosen because it is able to reduce the makespan of the jobs. Therefore, an deep MARL trained on these two objective will be used to benchmark against these existing dispatching rule.

## Deep reinforcement learning actor-critic (Stable baseline 3 + OpenAI Gym)
------------
## Reward Function design (Dense reward function)
All the rewards are normalised to [-1,1]
| Condition | Reward | Remarks | Goal | 
| ------------- | ------------- | ------------- | ------------- |
| Illegal actions | `-1` | If the agent take illegal action then we will penalise it | To teach the agent to take legal actions | 
| Processed Jobs | `+ 1 * time_processed` | For every unit of time that the job is processed, the agent receives a reward equivalent to the amount of processed time | To encourage agent to keep selecting jobs | 
| Machine idle time | `- 1 * time_idle` | For every unit time of machine being idle, the agent will be penalized | To minimize makespan | 
| Job past its due date | if late `-1/3` else `+1` | | To lower number of tardy jobs |

## Synchronous actor critic reinforcement learning (A2C from stable baseline 3) 
link : https://stable-baselines3.readthedocs.io/en/master/modules/a2c.html
| Configurations | Values | Remarks | 
| ------------- | ------------- | ------------- |
| Agent update interval (timesteps) | 500 | 
| Entrophy coefficient | 0.01 | To avoid being in local optima | This is used for loss calculation |
| Discount factor | 0.99 | To consider rewards from the next state | 
| Value function coefficient | 0.5 | This is used for loss calculation | 

### Multi - layer perceptron configurations (MLP - policy from stable baseline 3)
link : https://stable-baselines3.readthedocs.io/en/master/guide/custom_policy.html
| Configurations | Values | Remarks | 
| ------------- | ------------- | ------------- |
| Neural network layers | 2 | 
| Activation function | tanh() |
| Learning rate | 0.007 | 

### Deep actor-critic reinforcement learning results
## Comparing both Dispatching rule and Deep actor-critic reinforcement learning
### Tardy jobs comparison
**5000 Episodes**

| action_type | maximum allowable jobs | Number of tardy jobs in percentage per episode | 
| ------------- | ------------- | ------------- | 
| S_RPT + SPT | 25 | 25.5% |
| MTWR | 25 | 31.8% |
| A2C | 25 | 8.2% |
| S_RPT + SPT | 30 | 42.9%% |
| MTWR | 30 | 47.9%% |
| A2C | 30 | 25.4% |
| S_RPT + SPT | 35 | 57.7% |
| MTWR | 35 | 61.9% |
| A2C | 35 | 36.9% |
| S_RPT + SPT | 40 | 72.3% |
| MTWR | 40 | 73.4% |
| A2C | 40 | 57.2% |

### Makespan comparison, the makespan KDE plot is calculated from simulations with 5000 episodes.

#### **Performance for each individual scheduling methods at max_jobs =`25`**

<img src = "./Project/(FYP) Data/(PLOT) Makespan Adjusted/COMBINED_25_5000_makespan.png" weight = "60%" height = "60%">

#### **Performance for each individual scheduling methods at max_jobs =`30`**

<img src = "./Project/(FYP) Data/(PLOT) Makespan Adjusted/COMBINED_30_5000_makespan.png" weight = "60%" height = "60%">

#### **Performance for each individual scheduling methods at max_jobs =`35`**

<img src = "./Project/(FYP) Data/(PLOT) Makespan Adjusted/COMBINED_35_5000_makespan.png" weight = "60%" height = "60%">

#### **Performance for each individual scheduling methods at max_jobs =`40`**

<img src = "./Project/(FYP) Data/(PLOT) Makespan Adjusted/COMBINED_35_5000_makespan.png" weight = "60%" height = "60%">

## Project Organization
------------

    ├── README.md             <- The top-level README for developers using this project.
    ├── JSSEnv
    │   └── envs              <- Contains the environment.
    │       └── instances     <- Contains some intances from the litterature.
    |       ├── jss1_env.py   <- initial static JSSP environment   
    |       ├── djss_env.py   <- dynamic decorator generate dynamic job arrival
    |
    ├── (TESTING) automated_testing
    |    ├── automated_test.py <- this function automates my test by running n number of episode so that I can review their performance and get the result above
    |    ├── automated_test_log_xlsx <- this is to store my number of tardyness data in excel format which was generated by the automated_test.py 
    |    
    ├── Project
        ├── RL_environment.py <- This is where I generate the episodes.
        ├── Reward_Function.xlsx <- log book for the trained model 
        ├── Model <- contain all the differnt agent trained on different reward function, different environment configurations. The information are stored inside Reward_Function.xslx
        ├── model_logs <- Stores the tensorboard log for the deep a2c agent
        ├── (FYP) Data <- contains all the data that is shown in the README file
            ├── (PLOT) Makespan <- makespan plot that contain all the episodes, including those who terminated prematurely. 
            ├── (PLOT) Makespan Adjusted <- removed the episodes that terminates prematurely
--------


## License

MIT License
