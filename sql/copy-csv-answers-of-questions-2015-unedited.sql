Get a csv of answer in 2015 that are unedited and have corresponding questions after filtering the questions in the previous query:

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

select count(*)
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

972715

Time: 9299.029 ms

\copy (select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null and parentid in (select id from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 1 and lasteditdate is null)) TO '/tmp/answers-of-unedited-questions-2015.csv' WITH CSV HEADER
COPY 1
Time: 11381.596 ms\copy (select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null and parentid in (select id from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 1 and lasteditdate is null)) TO '/tmp/answers-of-unedited-questions-2015.csv' WITH CSV HEADER
COPY 972715
Time: 19023.390 ms