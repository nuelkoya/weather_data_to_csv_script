import os
import json
import shutil
from subprocess import PIPE, run
import sys
from types import new_class

GAME_DIR_PATTERN = "game"


def get_directories_from_source(source):
    all_directories = []
    for root, dirs, files in os.walk(source):
        for dir in dirs:
            if GAME_DIR_PATTERN in dir:
                all_directories.append(dir) 
        break
    return all_directories

def create_directory(source, target):
    dir_in_target = []
    for dir in source:
        new_path = dir.replace("_game", "")
        new_dir = os.path.join(target, new_path)
        dir_in_target.append(new_dir)
    
    return dir_in_target


def move_content(root_source, source, target):
    src_full = []
    for src in source:
        src_path = os.path.join(root_source,src)
        src_full.append(src_path)
    
    for src, dest in zip(src_full, target):
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src,dest)

def create_json(paths):
    data = {
        "Message": "This is a read me file"
        }

    for path in paths:
        json_path = os.path.join(path, "readme.json")
        with open(json_path, 'w') as f:
            json.dump(data, f)
    



def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    source_directories = get_directories_from_source(source_path)
    target_sub_directories = create_directory(source_directories, target_path)
    move_content(source_path, source_directories, target_sub_directories)
    create_json(target_sub_directories)
    #print(target_sub_directories)
    


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("Enter source and destination")
    source, target = args[1:]
    main(source, target)
    