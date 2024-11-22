import os

def create_dir(path: str) -> str:
    os.mkdir(path)
    return path