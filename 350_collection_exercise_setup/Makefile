default: ashe_201803 bricks_201801 misc qbs_1809 rsi_201812

ashe_201803:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < ashe_201803_setup.sql

bricks_201801:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < bricks_201801_setup.sql

misc:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < collection_exercise_setup_template.sql

qbs_1809:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < qbs_1809_setup.sql

rsi_201812:
	psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p${POSTGRES_PORT} ${POSTGRES_DB} < rsi_201812_setup.sql
