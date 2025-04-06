# Final Year Project - Dynamic Job-Shop Scheduling Environment 
An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

## Disclaimer 
------------
For my professor or PhD student reviewing my repository, please note that I have added a dynamic scheduling decorator on top of the existing static JSSP environment, which was originally developed by someone else. The dynamic scheduling decorator is a wrapper around the static JSSP class that enables the generation of dynamically arriving jobs.

However, I soon realized that testing and benchmarking in the dynamic environment require a large number of episodes (potentially more than 10,000) due to the randomness of job arrivals. Therefore, at this stage, a static JSSP will be used as a foundation for benchmarking existing dispatching rules and potentially a deep MARL (Multi-Agent Reinforcement Learning) actor-critic agent during the initial phase.

Once the deep MARL agent is set up, it will be applied to the dynamic JSSP environment, where benchmarking will be conducted over many episodes to compare the deep MARL approach with existing dispatching rules.

## Results 
------------
### Gif (Just demonstration for each dispatching rule)
I have implemented 3 most common dispatching rule in my dynamic JSSP environment, but only  S_RPT + SPT and MTWR will be used to benchmark against the deep multi agent reinforcement learning (MARL).
The objective of the deep MARL would be to minimize number of tardy jobs and makespan in a batch.

### Example of each dispatching rule per EPISODE
------------
1. First in first out (FIFO)

 ![GIF not loaded](./(GITHUB)%20Graphs/result_FIFO_schedule.gif)

2. S/RPT + SPT (Job Slack/Remaining Processing Time) combined with Shortest Processing Time

 ![GIF not loaded](./(GITHUB)%20Graphs/result_S_RPT_schedule.gif)

3. Most Total Work Remaining (MTWR)

 ![GIF not loaded](./(GITHUB)%20Graphs/result_MWTR_schedule.gif)

### DJSSP environment configuration
------------
The dynamic job scheduling environment is characteristed by these parameters: 
- **Number of Machines**: `6`
- **Maximum Allowable Jobs**: `25`
- **Processing Time Range**: `[50, 60]`
- **Allowable Number of Operations per Job**: `[5, 6]`
- **Due Date Tightness (α)**: `[10, 12]`
The variation between each variable are kept minimum to allow for a more stable result. 

### Number of tardy jobs
------------
In this table for multiple episodes, S_RPT + SPT is the best in reducing number of tardy jobs. 
| action_type | Number of Episode | Number of tardy jobs in percentage | 
| ------------- | ------------- | ------------- | 
| FIFO  | 1000 | 10.2% |
| S_RPT + SPT  | 1000 | 3.8% |
| MTWR  | 1000 | 6.7% | 
| FIFO  | 3000 | 9.8% |
| S_RPT + SPT  | 3000 | 4.0% |
| MTWR  | 3000  | 6.6% | 


### Makespan plotted on Kernal Density Estimation (KDE) for multiple EPISODES
------------
1. FIFO with 1000 episode

 <img src="./(GITHUB) Graphs/2025-03-13_18-17-53_FIFO_1000_makespan_kdeplot.png" width="60%" height="60%"/>

2. S_RPT + SPT with 1000 episode

 <img src="./(GITHUB) Graphs/2025-03-13_18-30-17_S_RPT_1000_makespan_kdeplot.png" width="60%" height="60%"/>

3. MTWR with 1000 episode

For 1000 episode, MTWR effective reduces makespan when compared with FIFO, but it performs similar as compared to S_RPT + SPT.

 <img src="./(GITHUB) Graphs/2025-03-13_18-40-25_MTWR_1000_makespan_kdeplot.png" width="60%" height="60%"/>

4. FIFO with 3000 episode

 <img src="./(GITHUB) Graphs/2025-03-13_19-10-34_FIFO_3000_makespan_kdeplot.png" width="60%" height="60%"/>

5. S_RPT + SPT with 3000 episode

 <img src="./(GITHUB) Graphs/2025-03-14_01-10-10_S_RPT_3000_makespan_kdeplot.png" width="60%" height="60%"/>
 
6. MTWR with 3000 episode

For 3000 episodes, this MTWR dominates both FIFO and S_RPT + SPT

 <img src="./(GITHUB) Graphs/2025-03-14_01-57-23_MTWR_3000_makespan_kdeplot.png" width="60%" height="60%"/>

### Conclusion
S_RPT + SPT is chosen because of its ability to reduce number of job tardiness. MTWR is chosen because it is able to reduce the makespan of the jobs. Therefore, an deep MARL trained on these two objective will be used to benchmark against these existing dispatching rule.

### Implementation deep actor critic reinforcement learning for dynamic JSSP (Stable baseline 3 + OpenAI Gym)
------------
To note that all our rewards are normalised to [-1,1]
## Reward Function design (Dense reward function)
| Condition | Reward | Remarks | Goal | 
| ------------- | ------------- | ------------- | ------------- |
| Illegal actions | `-1` | If the agent take illegal action then we will penalise it | To teach the agent to take legal actions | 
| Processed Jobs | `+ 1 * time_processed` | For every unit of time that the job is processed, the agent receives a reward equivalent to the amount of processed time | To encourage agent to keep selecting jobs | 
| Machine idle time | `- 1 * time_idle` | For every unit time of machine being idle, the agent will be penalized | To minimize makespan | 
| Job past its due date | if late `-1/3` else `+1` | | To lower number of tardy jobs |

## Synchronous actor critic reinforcement learning (A2C from stable baseline 3) 
| Configurations | Values | Remarks | 
| ------------- | ------------- | ------------- |
| Agent update interval (timesteps) | 500 | 
| Entrophy coefficient | 0.01 | To avoid being in local optima | This is used for loss calculation |
| Discount factor | 0.99 | To consider rewards from the next state | 
| Value function coefficient | 0.5 | This is used for loss calculation | 

### Multi - layer perceptron configurations (MLP - policy from stable baseline 3)
| Configurations | Values | Remarks | 
| ------------- | ------------- | ------------- |
| Neural network layers | 2 | 
| Activation function | tanh() |
| Learning rate | 0.007 | 

### Results


### YET TO DO 
1. Design reward function - in progress
2. Implement single agent deep RL with actor critic (A2C) framework - with sb3 and tune hyperparameter with rl-baseline3zoo
3. Implement multi agent deep RL with acrtor critic (A3C) - ❌. But I will write some aspect of this in the FYP papers, highlighting its benefits. Because implementing multiple actor critic requires the use of RLLib or PyTorch which is time intensive. 
4. Benchmark the single A2C RL agent with the dispatching rule (S_RPT + SPT) and MTWR

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
    ├── RL_environment.py <- This is where I generate the episodes.
    |
    |
    |
    
--------


## License

MIT License
