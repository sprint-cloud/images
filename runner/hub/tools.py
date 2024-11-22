import os

def create_dir(path: str, may_excist = True) -> str:
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if not may_excist:
            raise e
    except Exception as e:
        raise e
    return path