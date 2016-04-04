# A - Very good questions (with accepted answer, not closed, not deleted, score > 7) - 76,592
# B - Good  questions  (with  accepted  answer,  not  closed,  not deleted, score 1-6) - 1,033,676
# C - Bad questions (not closed, not deleted, score < 0) - 70,837
# D - Very bad questions (closed or deleted) - 81,854


# Questions Very Bad
COPY (
    select id, parentid, creationdate, score, viewcount,
           title, tags, answercount, commentcount,
           favoritecount, closeddate, communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 1 and
        lasteditdate is null and
        score < 0 and
        closeddate is not null
    order by RANDOM()
) TO '/tmp/questions-verybad.csv' WITH CSV HEADER;

COPY 28611


# Questions Bad
COPY (
    select id, parentid, creationdate, score,
           viewcount, title, tags, answercount,
           commentcount, favoritecount, closeddate,
           communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 1 and
        lasteditdate is null and
        score < 0 and
        closeddate is null
    order by RANDOM()
) TO '/tmp/questions-bad.csv' WITH CSV HEADER;

COPY 126436


# Questions Good
COPY (
    select id, parentid, creationdate, score,
           viewcount, title, tags, answercount,
           commentcount, favoritecount, closeddate,
           communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 1 and
        lasteditdate is null and
        closeddate is null and
        acceptedanswerid is not null and
        score > 0 and
        score <= 6
    order by RANDOM()
) TO '/tmp/questions-good.csv' WITH CSV HEADER;

COPY 404099


# Questions Very Good
COPY (
    select id, parentid, creationdate, score,
           viewcount, title, tags, answercount,
           commentcount, favoritecount, closeddate,
           communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 1 and
        lasteditdate is null and
        closeddate is null and
        acceptedanswerid is not null and
        score >= 7
    order by RANDOM()
) TO '/tmp/questions-verygood.csv' WITH CSV HEADER;

COPY 12534
