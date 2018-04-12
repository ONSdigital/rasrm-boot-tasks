default: env_production

# I am going to go with this being ok as it's setting an absolute value
export PYTHONPATH=${PWD}/lib
export LIBDIR=${PYTHONPATH}

env_production:
	PIPENV_DOTENV_LOCATION=$(PWD)/environment.production pipenv run python tasks.py --include=${INCLUDE_TASKS} --exclude=${EXCLUDE_TASKS}

env_test:
	PIPENV_DOTENV_LOCATION=$(PWD)/environment.test pipenv run python tasks.py --include=${INCLUDE_TASKS} --exclude=${EXCLUDE_TASKS}
