-- QBS action schema

INSERT INTO action.actiontype(
actiontypepk, name, description, handler, cancancel, responserequired)
VALUES (4,'BSNL','Business Survey Notification Letter','Printer',true,false)
ON CONFLICT (actiontypepk) DO NOTHING;

INSERT INTO action.actiontype(
actiontypepk, name, description, handler, cancancel, responserequired)
VALUES (5,'BSNE','Business Survey Notification Email','Notify',true,false)
ON CONFLICT (actiontypepk) DO NOTHING;
INSERT INTO action.actiontype(
actiontypepk, name, description, handler, cancancel, responserequired)
VALUES (6,'BSRL','Business Survey Reminder Letter','Printer',true,false)
ON CONFLICT (actiontypepk) DO NOTHING;
INSERT INTO action.actiontype(
actiontypepk, name, description, handler, cancancel, responserequired)
VALUES (7,'BSRE','Business Survey Reminder Email','Notify',true,false)
ON CONFLICT (actiontypepk) DO NOTHING;

INSERT INTO action.actionplan(
id, actionplanpk, name, description, createdby, lastrundatetime)
VALUES ('2eb53b02-1e1d-11e8-b467-0ed5f89f718b', 7, 'Quarterly Business Survey', 'Quarterly Business Survey B Case', 'Release 16', NULL)
ON CONFLICT (actionplanpk) DO NOTHING;

INSERT INTO action.actionplan(
id, actionplanpk, name, description, createdby, lastrundatetime)
VALUES ('5cbba6f8-1e1d-11e8-b467-0ed5f89f718b', 8, 'Quarterly Business Survey BI', 'Quarterly Business Survey BI Case', 'Release 16', NULL)
ON CONFLICT (actionplanpk) DO NOTHING;

INSERT INTO action.actionplan(
id, actionplanpk, name, description, createdby, lastrundatetime)
VALUES ('36148dbe-1e20-11e8-b467-0ed5f89f718b', 9, 'Quarterly Business Survey B 1803', 'Quarterly Business Survey B Case 1803', 'Release 16', NULL)
ON CONFLICT (actionplanpk) DO NOTHING;

INSERT INTO action.actionplan(
id, actionplanpk, name, description, createdby, lastrundatetime)
VALUES ('45a4e63e-1e20-11e8-b467-0ed5f89f718b', 10, 'Quarterly Business Survey BI 1803', 'Quarterly Business Survey BI Case 1803', 'Release 16', NULL)
ON CONFLICT (actionplanpk) DO NOTHING;

INSERT INTO action.actionrule(
actionrulepk, actionplanfk, actiontypefk, name, description, daysoffset, priority)
VALUES (6,9,4,'QBSNOT+0','QBS Enrolment Invitation Letter(+0 days)',10000,3)
ON CONFLICT (actionrulepk) DO NOTHING;



-- collectionexercise schema

INSERT INTO collectionexercise.casetypeoverride(casetypeoverridepk, exercisefk, sampleunittypefk, actionplanid)
SELECT 1, ce.exercisepk,'B', '36148dbe-1e20-11e8-b467-0ed5f89f718b'
FROM collectionexercise.collectionexercise ce
INNER JOIN survey.survey AS s ON ce.survey_uuid = s.id
WHERE s.shortname = 'QBS'
AND ce.exerciseref = '1803'
ON CONFLICT (casetypeoverridepk) DO NOTHING;

INSERT INTO collectionexercise.casetypeoverride(casetypeoverridepk, exercisefk, sampleunittypefk, actionplanid)
SELECT 2, ce.exercisepk, 'BI', '45a4e63e-1e20-11e8-b467-0ed5f89f718b'
FROM collectionexercise.collectionexercise ce
INNER JOIN survey.survey AS s ON ce.survey_uuid = s.id
WHERE s.shortname = 'QBS'
AND ce.exerciseref = '1803'
ON CONFLICT (casetypeoverridepk) DO NOTHING;
