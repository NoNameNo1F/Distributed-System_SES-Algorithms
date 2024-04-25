"""
    logging writes into file with specifics info, error, warn,...

"""
import os
from datetime import datetime

from .helpers import get_data_file_path


class Logging:
    def __init__(self, dir, filename):
        self._path = get_data_file_path(dir, filename)

    def Log(self, message, status):
        if status in ["ERROR", "INFO", "WARNING"]:
            print(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}\n")
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            with open(self._path, "a+") as output_file:
                output_file.write(f"{datetime.now().strftime('%m-%d-%Y %I:%M:%S.%f %p')} - {status} - {message}\n")
