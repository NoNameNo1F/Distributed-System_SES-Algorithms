"""
    Helpers:
        get_absolute_file_path()
        ...
"""
import os


def get_data_file_path(dir, filename):
    # Get the path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, dir)
    # Return the path to the data.json file
    return os.path.join(data_dir, filename)
