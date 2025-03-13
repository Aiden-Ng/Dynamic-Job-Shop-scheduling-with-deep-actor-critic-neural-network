# Final Year Project - Dynamic Job-Shop Scheduling Environment 
An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

## Results 
------------
I have implemented 3 most common dispatching rule in my dynamic JSSP environment. 

### Makespan
1. First in first out (FIFO)
![GIF not loaded](./result_FIFO_schedule.gif)

3. S/RPT + SPT (Job Slack/Remaining Processing Time) combined with Shortest Processing Time
![GIF not loaded](./result_S_RPT_schedule.gif)

5. Most Total Work Remaining (MTWR)
![GIF not loaded](./result_MWTR_schedule.gif)

### Number of tardy jobs
| Method | Number of Episode | Number of tardy jobs in percentage | 
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
