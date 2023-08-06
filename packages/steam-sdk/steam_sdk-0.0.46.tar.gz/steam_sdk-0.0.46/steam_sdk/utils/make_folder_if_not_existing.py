import os
from pathlib import Path


def make_folder_if_not_existing(folder: str, verbose: bool = False):
    if not os.path.isdir(folder):
        Path(folder).mkdir(parents=True, exist_ok=True)
        if verbose:
            print("Folder {} does not exist. Making it now".format(folder))