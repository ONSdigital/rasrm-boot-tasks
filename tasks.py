import os
import logging
import subprocess

INVALID_PRIORITY = -1
MAKEFILE_NAME = "Makefile"

def get_task_directory_priority(name):
    result = INVALID_PRIORITY
    tokens = name.split("_")
    if len(tokens) > 1:
        priority = tokens[0]

        try:
            result = int(priority)
        except ValueError:
            result = INVALID_PRIORITY

    return result
        
def get_makefile_path(task_directory):
    return "{}/{}".format(task_directory, MAKEFILE_NAME)
    
def is_task_directory(name):
    priority = get_task_directory_priority(name)
    makefile_path = get_makefile_path(name)
    has_makefile = os.path.isfile(makefile_path)

    # If it looks like it should be a task directory but isn't then log a warning
    if priority != INVALID_PRIORITY and not has_makefile:
        logging.warning("Directory {} has no {}".format(name, MAKEFILE_NAME))

    return priority != INVALID_PRIORITY and has_makefile

def execute_task_directory(task_directory):
    logging.info("=" * 120)
    logging.info("Executing: {}".format(task_directory))
    logging.info("=" * 120)
    makefile_path = get_makefile_path(task_directory)
    logging.debug("makefile_path: {}".format(makefile_path))
    
    subprocess.run(["make", "-f", MAKEFILE_NAME], cwd=task_directory)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dirnames = next(os.walk('.'))[1]
    filtered = filter(is_task_directory, dirnames)
    s = sorted(filtered, key=get_task_directory_priority)

    [execute_task_directory(task_dir) for task_dir in s]

