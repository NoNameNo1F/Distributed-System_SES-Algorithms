"""
    Helpers:
        get_absolute_file_path()
        ...
"""
import os


def get_foldershares_path():
    """
        Function: get foldershares path
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, '../../FolderShares')
    return os.path.normpath(path)

def get_data_file_path(dir, filename):
    """
        Get specific file path
    """
    # Get the path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, dir)
    # Return the path to the data.json file
    path = os.path.join(data_dir, filename)
    return os.path.normpath(path)

def create_folders(site_folder, site_subfolders, other_sites_subfolders):
    """
        setup folder to mounting when initializing connection
    """
    # Create the main folder
    parent_folder = get_foldershares_path()
    main_path = os.path.join(parent_folder, site_folder)
    os.makedirs(main_path, exist_ok=True)

    # Create subfolders inside the main folder
    for folder in site_subfolders:
        os.makedirs(os.path.join(main_path, folder), exist_ok=True)

        # If the subfolder is 'OtherSites', create additional subfolders
        if folder == 'OtherSites':
            for subfolder in other_sites_subfolders:
                os.makedirs(os.path.join(main_path, folder, subfolder), exist_ok=True)
