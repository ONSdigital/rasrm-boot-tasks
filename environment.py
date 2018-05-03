import logging

DEFAULT_ENVIRONMENT_FILE = "environment.production"
ENVIRONMENT_FILE_DELIMITER = "="

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

if __name__ == '__main__':
    logging.info("Library for reading in environment files"
