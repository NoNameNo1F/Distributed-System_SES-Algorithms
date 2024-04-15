"""
    logging writes into file with specifics info, error, warn,...

"""
import os
from datetime import datetime

from utils.helpers import get_data_file_path


class Logging:
    def __init__(self, dir, filename):
        self._path = get_data_file_path(dir, filename)

    def Log(self, message, status):
        if status in ["ERROR", "INFO", "WARNING"]:
            print(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}")
            with open(self._path, "w") as output_file:
                output_file.write(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}\n")
