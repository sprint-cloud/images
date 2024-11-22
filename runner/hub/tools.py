import os, time

def create_dir(path: str, may_excist = True) -> str:
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if not may_excist:
            raise e
    except Exception as e:
        raise e
    return path

def create_temp_dir(prefix: str = "hub"):
    dirname = "{}_{}".format(prefix, time.time())
    path = os.path.join('/tmp/', dirname)
    return create_dir(path, may_excist=False)
