default:
	pipenv run python ../lib/load_events.py config/${OFATS_EVENT_LOAD_CONFIG} \
		--posturl=http://${COLLEX_HOST}:${COLLEX_PORT}/collectionexercises/{id}/events \
		--geturl=http://${COLLEX_HOST}:${COLLEX_PORT}/collectionexercises/{exercise_ref}/survey/{survey_ref} \
		--user=${COLLEX_USER} --password ${COLLEX_PASSWORD}
