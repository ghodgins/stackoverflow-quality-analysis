Get a csv of questions in 2015 that are unedited:
\copy (
	select id, acceptedanswerid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 1 and lasteditdate is null)
	TO '/tmp/questions-unedited-2015.csv' WITH CSV HEADER
COPY 1271230
Time: 12331.783 ms