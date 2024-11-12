import pathlib

def file_exists(request_uri):
    file_path = pathlib.Path(request_uri)
    return list(file_path.parent.glob(file_path.name + ".*"))
