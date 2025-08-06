from io import TextIOWrapper
import os
from pyray import file_exists

def open_save_file(open_mode:str = "r") -> tuple[TextIOWrapper, list[str]]:
    contents = []
    
    while not file_exists("PersistentData\\Save_Data.txt"):
        pass

    while len(contents) < 4:
        contents.clear()
        # renaming a file can sometimes cause permission errors for a few frames, so keep trying until success
        while True:  
            # make this process wait for the saving process to finish
            if file_exists("PersistentData\\Save_Data.txt"):
                try:
                    # open and get file data
                    os.rename("PersistentData\\Save_Data.txt", "PersistentData\\Save_Data.saving")
                except:
                    pass
            
            if file_exists("PersistentData\\Save_Data.saving"):
                try:
                    file:TextIOWrapper = open("PersistentData\\Save_Data.saving", open_mode)
                    break
                except:
                    pass

        contents = [line.strip() for line in file if line.strip()]

    if open_mode == "r+":
        file.seek(0)
        file.truncate()
    
    return file, contents

def close_save_file(file:TextIOWrapper) -> None:

    file.close()
    
    while True:
        try:
            os.rename("PersistentData\\Save_Data.saving", "PersistentData\\Save_Data.txt")
            break
        except:
            pass

def get_save_contents() -> list[str]:
     file, contents = open_save_file()
     close_save_file(file)
     return contents