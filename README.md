# Final Year Project - Dynamic Job-Shop Scheduling Environment 
An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

## Results 
------------
### Gif (Just demonstration for each dispatching rule)
I have implemented 3 most common dispatching rule in my dynamic JSSP environment. 

### Makespan
------------
1. First in first out (FIFO)
![GIF not loaded](./result_FIFO_schedule.gif)
2. S/RPT + SPT (Job Slack/Remaining Processing Time) combined with Shortest Processing Time
![GIF not loaded](./result_S_RPT_schedule.gif)
3. Most Total Work Remaining (MTWR)
![GIF not loaded](./result_MWTR_schedule.gif)

### Number of tardy jobs
------------
The dynamic job scheduling environment is characteristed by these parameters: 
- **Number of Machines**: `6`
- **Maximum Allowable Jobs**: `25`
- **Processing Time Range**: `[50, 60]`
- **Allowable Number of Operations per Job**: `[5, 6]`
- **Due Date Tightness (α)**: `[10, 12]`
The variation between each variable are kept minimum to allow for a more stable result. 

| action_type | Number of Episode | Number of tardy jobs in percentage | 
| ------------- | ------------- | ------------- | 
| FIFO  | Content Cell  |
| S_RPT + SPT  | Content Cell  |
| MTWR  | Content Cell  |
| FIFO  | Content Cell  |
| S_RPT + SPT  | Content Cell  |
| MTWR  | Content Cell  |
| FIFO  | Content Cell  |
| S_RPT + SPT  | Content Cell  |
| MTWR  | Content Cell  |


Project Organization
------------

    ├── README.md             <- The top-level README for developers using this project.
    ├── JSSEnv
    │   └── envs              <- Contains the environment.
    │       └── instances     <- Contains some intances from the litterature.
    │
  
--------


## License

MIT License
