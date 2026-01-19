import time
import os

def tail_file(filename):
    """It goes to end of the document and waiting to new lines"""
    try:
        with open(filename, 'r') as f:
            # go to end of the file
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1) # do not tired to processor
                    continue
                yield line

    except FileNotFoundError:
        print(f"Error: {filename} not found")
    except PermissionError:
        print(f"Error: {filename} permission denied")
