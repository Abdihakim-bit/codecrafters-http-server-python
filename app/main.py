from .server import start_server
import pathlib
import sys

if __name__ == "__main__":
    try:
        base_directory = sys.argv[2]
    except IndexError:
        base_directory = str(pathlib.Path().absolute())
    start_server(base_directory)