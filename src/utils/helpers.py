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

def create_folder(port):
    site_folder = f"Site{port}"
    os.makedirs(site_folder, exist_ok=True)

    peer_folder = os.path.join(site_folder, f"Peer{port}")
    os.makedirs(peer_folder, exist_ok=True)
