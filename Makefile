default: env_production

env_production:
	pipenv run python tasks.py --env=environment.production

env_test:
	pipenv run python tasks.py --env=environment.test

test_task:
    pipenv run python tasks.py --env=environment.test --include=${PRIORITY}
