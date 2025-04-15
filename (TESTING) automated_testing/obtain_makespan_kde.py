import pandas as pd
import numpy as np
from pathlib import Path

#obtain the pandas df
ACTION_TYPE = "S_RPT"
MAX_JOBS = 25

EXCEL_PATH = (Path(__file__).parent / ".."/ ".."/ ".."/ ".."/ rf"{ACTION_TYPE}_{MAX_JOBS}_makespan.csv").resolve()
df = pd.read_csv(EXCEL_PATH)


def main():
    pass

main()