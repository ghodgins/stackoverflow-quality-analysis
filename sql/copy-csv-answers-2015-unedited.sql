Get a csv of answers in 2015 that are unedited:
\copy (select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null) TO '/home/ghodgins/Dissertation/stackoverflow-quality-analysis/data/answers-unedited-2015.csv' WITH CSV HEADER
COPY 2318564
Time: 15331.783 ms





COPY (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where
		creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 2 and
		lasteditdate is null
) TO '/tmp/answers-unedited-2015.csv' WITH CSV HEADER
