default:
	pipenv run python load_events.py config/${COLLEX_EVENT_LOAD_CONFIG} \
		--posturl=http://${COLLEX_HOST}:${COLLEX_PORT}/collectionexercises/{id}/events \
		--geturl=http://${COLLEX_HOST}:${COLLEX_PORT}/collectionexercises/{exercise_ref}/survey/{survey_ref} \
		--user=${COLLEX_USER} --password ${COLLEX_PASSWORD}
