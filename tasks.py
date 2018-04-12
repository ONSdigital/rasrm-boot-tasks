import os
import logging
import subprocess
import argparse
from functools import partial

INVALID_PRIORITY = -1
MAKEFILE_NAME = "Makefile"
DEFAULT_ENVIRONMENT_FILE = "environment.production"
ENVIRONMENT_FILE_DELIMITER = "="

def parse_args():
    parser = argparse.ArgumentParser(description='Automated RAS/RM initialisation tasks')
    parser.add_argument("--environment", help="Environment file to load", nargs='?', default=DEFAULT_ENVIRONMENT_FILE)
    parser.add_argument("--exclude", help="Tasks to exclude (priority list)", nargs='?')
    parser.add_argument("--include", help="Tasks to include (priority list)", nargs='?')
    parser.add_argument('--test', help="Test mode - don't execute any tasks", dest='test', action='store_true')
    return parser.parse_args()

def log_separator():
    logging.info("=" * 200)

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

# Make target can be specified in environment by defining variable
# task_directory_target (e.g. 50_Print_Environment_target=alternative)
def get_make_target(task_directory, env):
    make_target = None
    make_target_var = "{}_target".format(task_directory)

    try: 
        make_target = env[make_target_var]
    except KeyError:
        make_target = None

    return make_target

def execute_task_directory(task_directory,env):
    logging.info("Executing: {}".format(task_directory))
    log_separator()
    makefile_path = get_makefile_path(task_directory)
    logging.debug("makefile_path: {}".format(makefile_path))

    cmdline = ["make", "-f", MAKEFILE_NAME]

    make_target = get_make_target(task_directory, env)

    if make_target:
        logging.info("Using make target {}".format(make_target))
        cmdline.append(make_target)
    else:
        logging.info("Using default make target")
    
    subprocess.run(cmdline, cwd=task_directory, env=env)

def parse_environment_file_line(line):
    try:
        new_line = line.strip()

        if new_line and not new_line.startswith("#"):
            index = new_line.index(ENVIRONMENT_FILE_DELIMITER)

            return True, new_line[:index].strip(), new_line[index+1:].strip()
        else:
            return False, None, None
    except: 
        logging.error("Error parsing line {}".format(line))
        raise 

    
def read_environment_file(args):
    logging.info("Environment file: {}".format(args.environment))
    if not os.path.isfile(args.environment):
        raise ValueError("Environment file {} does not exist".format(args.environment))

    new_env = os.environ.copy()

    file = open(args.environment, "r")
    for line in file:
        try:
            valid, key, value = parse_environment_file_line(line)

            if valid:
                new_env[key] = value
        except ValueError:
            logging.warning("Invalid environment definition: {}".format(line))

    return new_env

def parse_priority_list(priority_list_str):
    if priority_list_str:
        priority_str_list = priority_list_str.split(",")

        return [int(priority_str) for priority_str in priority_str_list]
    else:
        return None

def is_task_enabled(task_dir, include, exclude):
    priority = get_task_directory_priority(task_dir)

    return (not include or priority in include) and (not exclude or not priority in exclude)

def get_include_exclude(args):
    return parse_priority_list(args.include), parse_priority_list(args.exclude)

def handle_task(task_dir, enabled_fn, test, env_dict):
    log_separator()
    enabled = enabled_fn(task_dir)
    
    if enabled:
        if not test:
            execute_task_directory(task_dir, env_dict)
        else:
            logging.info("Not Executing: {} - TEST MODE".format(task_dir))
    else:
        logging.info("Not Executing: {} - DISABLED".format(task_dir))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    include, exclude = get_include_exclude(args)
    logging.info("Include tasks: {}".format(include))
    logging.info("Exclude tasks: {}".format(exclude))

    env_dict = read_environment_file(args)
    
    dirnames = next(os.walk('.'))[1]
    filtered = filter(is_task_directory, dirnames)
    s = sorted(filtered, key=get_task_directory_priority)

    enabled_fn = partial(is_task_enabled, include=include, exclude=exclude)

    [handle_task(task_dir, enabled_fn, args.test, env_dict) for task_dir in s]

