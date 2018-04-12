default: env_production

env_production:
	PIPENV_DOTENV_LOCATION=$(PWD)/environment.production pipenv run python tasks.py

env_test:
	PIPENV_DOTENV_LOCATION=$(PWD)/environment.test pipenv run python tasks.py

test_task:
    PIPENV_DOTENV_LOCATION=$(PWD)/environment.test pipenv run python tasks.py --include=${PRIORITY}
