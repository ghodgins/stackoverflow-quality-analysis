select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00' and
    posttypeid = 2 and
    lasteditdate is null and
    parentid in (
    	select id
    	from posts
    	where
    	    creationdate >= timestamp '2015-01-01 00:00:00' and
    	    creationdate < timestamp '2016-01-01 00:00:00' and
    	    posttypeid = 1 and
    	    lasteditdate is null
    );



# Answers Very Bad
COPY (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where
		creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 2 and
		lasteditdate is null and
		score < 0
) TO '/tmp/answers-verybad.csv' WITH CSV HEADER

# Answers Bad
COPY (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where
		creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 2 and
		lasteditdate is null and
		score < 0
) TO '/tmp/answers-bad.csv' WITH CSV HEADER

# Answers Good
COPY (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where
		creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 2 and
		lasteditdate is null and
		score > 0 and
		score < 7
) TO '/tmp/answers-good.csv' WITH CSV HEADER

# Answers Very Good
COPY (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where
		creationdate >= timestamp '2015-01-01 00:00:00' and
		creationdate < timestamp '2016-01-01 00:00:00' and
		posttypeid = 2 and
		lasteditdate is null and
		score >= 7
) TO '/tmp/answers-verygood.csv' WITH CSV HEADER