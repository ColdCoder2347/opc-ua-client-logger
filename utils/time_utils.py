from datetime import datetime
import os


def get_current_logfile(log_dir="logs"):
    """Return full path for current hour's log file"""
    now = datetime.now()
    filename = f"OPC_Log_{now.strftime('%Y-%m-%d_%H')}.csv"
    return os.path.join(log_dir, filename)
