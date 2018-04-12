# rasrm-boot-tasks
A repo to hold all the initialisation tasks that need to be performed at RAS/RM startup (after service initialisation)

# Running the tasks

## TL;DR

### Production environment 

```
make
```

### Test environment 

```
make env_test
```

## tasks.py

The tasks are run by a Python script called tasks.py. 

```
pipenv run python tasks.py --help

usage: tasks.py [-h] [--environment [ENVIRONMENT]] [--exclude [EXCLUDE]]
                [--include [INCLUDE]] [--test]

Automated RAS/RM initialisation tasks

optional arguments:
  -h, --help            show this help message and exit
  --environment [ENVIRONMENT]
                        Environment file to load
  --exclude [EXCLUDE]   Tasks to exclude (priority list)
  --include [INCLUDE]   Tasks to include (priority list)
  --test                Test mode - don't execute any tasks
```

| Parameter     | Description |
|---------------|-------------|
| --environment | Specifies a file that contains environment variable definitions in the form KEY=VALUE that are passed to each of the tasks (defaults to environment.production) |
| --exclude | A comma-delimited list of integers specifying the task priorities to exclude (defaults to none) |
| --include | A comma-delimited list of integers specifying the task priorities to include (defaults to all) |
| --test | A flag to indicate the script is being run in test mode and no tasks should actually be run |

# Creating a new task

New tasks must:

- be idempotent
- work in both cloud foundry and local docker environments

## Create the task directory

Task directories are named as follows: 

```
priority_description
```

The priority must be an integer.  The first underscore is mandatory (necessary to identify the priority).  The description may contain any characters valid in a directory name but *THE USE OF SPACES IS STRONGLY DISCOURAGED*

Tasks are run in the numeric order of their priority.  Generally it is safest to add a new task at the end (i.e. give it a higher priority than any of the existing tasks).  

## Create a Makefile

tasks.py simply executes the Makefile present in the task directory.  So in order for the task to do something, a Makefile containing a useful default task must be created in the task directory.  If additional information needs to be passed through, see the next section.  

## Adding environment specific information

When tasks.py is run, it loads a specified environment file whose contents are passed to each of the tasks in turn.  If you need to pass environment specific information, you need to add it to one or all of the environment files (currently environment.production and envirionment.test).  These values can then be accessed from the Makefile as ${VARIABLE_NAME}.

## Testing 

The new task can be tested as follows:

```
PRIORITY=<new task priority> make test_task
```

This will run just the new task (well, and any that coincidentally share the same priority).
