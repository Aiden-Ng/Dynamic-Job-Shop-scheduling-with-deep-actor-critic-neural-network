# Final Year Project - Dynamic Job-Shop Scheduling Environment 

An optimized OpenAi gym's environment to simulate the Dynamic Job Shop Scheduling Problem

![til](./tests/ta01.gif)

Results 
------------
I have implemented 3 most common dispatching rule in my dynamic JSSP environment. 
1. First in first out (FIFO)

2. S/RPT + SPT (Job Slack/Remaining Processing Time) combined with Shortest Processing Time

3. Most Total Work Remaining (MTWR)

Project Organization
------------

    ├── README.md             <- The top-level README for developers using this project.
    ├── JSSEnv
    │   └── envs              <- Contains the environment.
    │       └── instances     <- Contains some intances from the litterature.
    │
    └── tests                 
        │
        ├── test_state.py     <- Unit tests focus on testing the state produced by
        │                        the environment.
        │
        ├── test_rendering.py <- Unit tests for the rendering, mainly used as an example
        |                        how to render the environment.
        │
        └── test_solutions.py <- Unit tests to ensure that our environment is correct checking
                                 known solution in the litterature leads to the intended make-
                                 span. We also check if all actions provided by the solution are
                                 legal in our environment.
--------


## License

MIT License
