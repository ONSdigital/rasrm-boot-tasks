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
PIPENV_DOTENV_LOCATION=`pwd`/environment.test pipenv run python tasks.py

usage: tasks.py [-h] [--exclude [EXCLUDE]] [--include [INCLUDE]] [--test]

Automated RAS/RM initialisation tasks

optional arguments:
  -h, --help           show this help message and exit
  --exclude [EXCLUDE]  Tasks to exclude (priority list)
  --include [INCLUDE]  Tasks to include (priority list)
  --test               Test mode - don't execute any tasks
```

| Parameter     | Description |
|---------------|-------------|
| --exclude | A comma-delimited list of integers specifying the task priorities to exclude (defaults to none) |
| --include | A comma-delimited list of integers specifying the task priorities to include (defaults to all) |
| --test | A flag to indicate the script is being run in test mode and no tasks should actually be run |

## Specifying an environment

tasks.py relies on the environment variable support provided by pipenv.  To run tasks.py with a specific environment file, the following command should be used:
```
PIPENV_DOTENV_LOCATION=<full-path-to-environment-file> pipenv run python tasks.py
```

The following approach can be used to specify an environment file present in the rasrm-boot-tasks directory:
```
PIPENV_DOTENV_LOCATION=$(PWD)/<environment-file-name> pipenv run python tasks.py
```

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

If you need to pass environment specific information, you need to add it to one or all of the environment files (currently environment.production and envirionment.test).  These values can then be accessed from the Makefile as ${VARIABLE_NAME}.

## Testing 

The new task can be tested as follows:

```
INCLUDE_TASKS=<new task priority> make env_test
```

This will run just the new task (well, and any that coincidentally share the same priority).

## Creating tasks to execute arbitrary SQL

Note: this assumes that the psql utility is installed on the target machine

An example of a SQL task can be found in the 300_release_16_sql_1 task directory.   Place any SQL scripts you wish to execute into the task directory then add the following lines to your Makefile.

```
default:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < your_sql_script.sql
```

The default Postgres credentials will most likely already be defined in your environment file.  If you need anything unusual, you can always define your own and use the default as a template.

## Create tasks to execute batch HTTP requests

There is a script within the lib directory that allows the batching of HTTP requests via a simple data format defined in JSON.  In order to execute one or more HTTP requests you need to create a file in the JSON format specified in the subsection, put it into the newly created task directory and add the following lines to the Makefile:

```
default:
	pipenv run python $(LIBDIR)/batch_http.py upload_eq_collection_instrument.json --host ${YOUR_HOST} --port ${YOUR_PORT} --username ${YOUR_USERNAME} --password ${YOUR_PASSWORD} 
```

Environment variables for your endpoint will need to be added to the environment file, unless it's an endpoint that is already supported.

### HTTP Batch Requester command line parameters

```
usage: batch_http.py [-h] --username USERNAME --password PASSWORD --host HOST
                     --port PORT [--scheme SCHEME]
                     file

Batch HTTP Loader

positional arguments:
  file                 JSON batch file to load

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Basic auth username
  --password PASSWORD  Basic auth password
  --host HOST          HTTP host
  --port PORT          HTTP port
  --scheme SCHEME      HTTP port
```

### HTTP Batch Requester JSON Data Format

| Field name | Field Description                                                                                           |
|------------|-------------------------------------------------------------------------------------------------------------|
| method     | HTTP method - currently GET, POST and PUT are supported but others can be easily added                      |
| context    | The address of the resource within the context of the server (i.e. minus scheme, host and port information) |
| headers    | A dictionary of headers to be passed with the request                                                       |
| payload    | Either a raw string or further JSON defining the body of the request                                        |
| params     | Query string parameters to be sent with the request                                                         |

#### Example of PUT request with JSON payload body

```
[{
		"method": "PUT",
		"context": "/templates/7e5df14d-fe38-4d27-8f54-436da64ec932",
		"headers": {
			"Content-Type": "application/json"
		},
		"payload": {
			"label": "GovERD Notification (GB)",
			"id": "7e5df14d-fe38-4d27-8f54-436da64ec932",
			"classification": {
				"LEGAL_BASIS": "GovERD",
				"COMMUNICATION_TYPE": "NOTIFICATION"
			},
			"uri": "001c09be-6095-4d09-aed1-bf8197b5d0f9",
			"type": "EMAIL"
		}
}]
```

#### Example of POST request with form encoded URL parameters

```
[{
		"method": "POST",
        "context": "/collection-instrument-api/1.0.2/upload",
		"params": {
            "classifiers": "{\"form_type\": \"0001\", \"eq_id\": \"2\"}",
            "survey_id": "02b9c366-7397-42f7-942a-76dc5876d86d"
		}
}]
```
