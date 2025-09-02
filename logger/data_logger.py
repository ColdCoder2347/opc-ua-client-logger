import os
import pandas as pd
from utils.time_utils import get_current_logfile


class DataLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, row):
        """Append a row of data to the current hourly log file"""
        logfile = get_current_logfile(self.log_dir)

        # Initialize file if not exists
        if not os.path.exists(logfile):
            header = ["Timestamp(ISO)", "Timestamp(EpochUTC)"] + [f"Tag{i+1}" for i in range(10)]
            pd.DataFrame(columns=header).to_csv(logfile, index=False)

        # Append row
        pd.DataFrame([row]).to_csv(logfile, mode="a", header=False, index=False)
