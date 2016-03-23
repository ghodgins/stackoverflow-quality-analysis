stackoverflow=# \d posts
 id                    | integer                     | not null
 posttypeid            | integer                     | not null
 acceptedanswerid      | integer                     |
 parentid              | integer                     |
 creationdate          | timestamp without time zone | not null
 score                 | integer                     |
 viewcount             | integer                     |
 body                  | text                        |
 owneruserid           | integer                     |
 lasteditoruserid      | integer                     |
 lasteditordisplayname | text                        |
 lasteditdate          | timestamp without time zone |
 lastactivitydate      | timestamp without time zone |
 title                 | text                        |
 tags                  | text                        |
 answercount           | integer                     |
 commentcount          | integer                     |
 favoritecount         | integer                     |
 closeddate            | timestamp without time zone |
 communityowneddate    | timestamp without time zone |


Count of posts per month:
select extract(month from creationdate), count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00'
group by extract(month from creationdate);
         1 | 438194
         2 | 442834
         3 | 495834
         4 | 504154
         5 | 490330
         6 | 493856
         7 | 514021
         8 | 477884
         9 | 468747
        10 | 488611
        11 | 465565
        12 | 471159

Count of questions per month:
select extract(month from creationdate), count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00' and
    posttypeid = 1
group by extract(month from creationdate);
         1 | 190817
         2 | 194718
         3 | 220703
         4 | 216005
         5 | 211512
         6 | 216252
         7 | 225387
         8 | 209578
         9 | 206034
        10 | 217194
        11 | 208293
        12 | 214011

Count of answers per month:
select extract(month from creationdate), count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00' and
    posttypeid = 2
group by extract(month from creationdate);
         1 | 246439
         2 | 247352
         3 | 274099
         4 | 287118
         5 | 277742
         6 | 276126
         7 | 287794
         8 | 267554
         9 | 261927
        10 | 270683
        11 | 256310
        12 | 256484

Unedited question count:
select count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00' and
    posttypeid = 1 and
    lasteditdate is null;
 1271230

Edited question cound:
select count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00'	and
    posttypeid = 1 and
    lasteditdate is not null;
 1259274

Total questions:
select count(*) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 1;
 2530504

Unedited answer count:
select count(*) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null;
 2318564

Time: 2778.682 ms

Edited answer count:
select count(*) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is not null;
 891064

Time: 2641.647 ms

Total answers:
select count(*) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2;
 3209628

Time: 2734.252 ms



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

Get a csv of answers in 2015 that are unedited:
\copy (
	select id, parentid, creationdate, score, viewcount, title, tags, answercount, commentcount, favoritecount, closeddate, communityowneddate, body
	from posts
	where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null)
	TO '/tmp/answers-unedited-2015.csv' WITH CSV HEADER
COPY 2318564
Time: 15331.783 ms

Get a csv of answer in 2015 that are unedited and have corresponding questions after filtering the questions in the previous query:

select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 2 and lasteditdate is null and parentid in (select id from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00' and posttypeid = 1 and lasteditdate is null);

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



Correlation between viewcount and score:
select corr(viewcount, score) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00';
 0.43960496811704
