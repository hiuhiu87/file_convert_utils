import os


def get_folder_save_file():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
