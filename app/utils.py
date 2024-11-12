import pathlib

# Check for the existence of files with any extension
def file_exists(request_uri):
    file_path = pathlib.Path(request_uri)
    return list(file_path.parent.glob(file_path.name + ".*"))
