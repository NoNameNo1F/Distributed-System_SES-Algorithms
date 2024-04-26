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

def get_peer_folder(peerSite) -> str:
    """
        Return path: /FolderShares/FolderSiteX/PeerSiteX
    """
    #peerSite is a name of Site: like Site1,Site2,...
    parent_path = get_foldershares_path()
    # get FolderSiteX
    folder_peer = os.path.join(parent_path, f"Folder{peerSite}")
    # get PeerSiteX
    main_folder_peer = os.path.join(folder_peer, f"Peer{peerSite}")
    return main_folder_peer

def get_otherpeer_folder(peerSite, receiverSite) -> str:
    """
        Return path: /FolderShares/FolderSiteX/OtherSites/SharePeerSiteX
    """
    #peerSite is a name of Site: like Site1,Site2,...
    parent_path = get_foldershares_path()
    # get FolderSiteX
    folder_otherpeer = os.path.join(parent_path, f"Folder{peerSite}")
    # get OtherSiteX
    other_folder_peer = os.path.join(folder_otherpeer, f"OtherSites")
    # get particular receiverSiteX
    share_peer_site = os.path.join(other_folder_peer, f"SharePeer{receiverSite}")
    return share_peer_site

def get_data_file_path(dir, filename) -> str:
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

def is_filename_exists(file_path: str) -> bool:
    """
        Return True if file_path exists
    """
    return os.path.exists(file_path)

def read_data_from_file(file_path: str) -> str:

    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_data_to_file(file_path: str, content: str) -> str:
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'a') as file:
        file.writelines(content)
    return content

def get_files_in_folder(folder_path) -> list:
    file_names = []
    for _, _, files in os.walk(folder_path):
        file_names.extend(files)

    return file_names
