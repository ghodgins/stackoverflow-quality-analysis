
# Answers Very Bad
COPY (
    select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 2 and
        lasteditdate is null and
        score <= -2 and
        parentid in (
            select id
            from posts
            where
                creationdate >= timestamp '2014-01-01 00:00:00' and
                creationdate < timestamp '2016-01-01 00:00:00' and
                posttypeid = 1 and
                lasteditdate is null
       )
    order by RANDOM()
) TO '/tmp/answers-verybad.csv' WITH CSV HEADER;

COPY 4958
Time: 2035.270 ms


# Answers Bad
COPY (
    select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 2 and
        lasteditdate is null and
        score = -1 and
        parentid in (
            select id
            from posts
            where
                creationdate >= timestamp '2014-01-01 00:00:00' and
                creationdate < timestamp '2016-01-01 00:00:00' and
                posttypeid = 1 and
                lasteditdate is null
        )
    order by RANDOM()
) TO '/tmp/answers-bad.csv' WITH CSV HEADER;

COPY 25655
Time: 2802.053 ms


# Answers Good
COPY (
    select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 2 and
        lasteditdate is null and
        score > 0 and
        score <= 6 and
        parentid in (
            select id
            from posts
            where
                creationdate >= timestamp '2014-01-01 00:00:00' and
                creationdate < timestamp '2016-01-01 00:00:00' and
                posttypeid = 1 and
                lasteditdate is null
        )
    order by RANDOM()
) TO '/tmp/answers-good.csv' WITH CSV HEADER;

COPY 995261
Time: 76698.192 ms


# Answers Very Good
COPY (
    select id, parentid, creationdate, score, viewcount, title, tags, commentcount, favoritecount, closeddate, communityowneddate, body
    from posts
    where
        creationdate >= timestamp '2014-01-01 00:00:00' and
        creationdate < timestamp '2016-01-01 00:00:00' and
        posttypeid = 2 and
        lasteditdate is null and
        score >= 7 and
        parentid in (
            select id
            from posts
            where
                creationdate >= timestamp '2014-01-01 00:00:00' and
                creationdate < timestamp '2016-01-01 00:00:00' and
                posttypeid = 1 and
                lasteditdate is null
        )
    order by RANDOM()
) TO '/tmp/answers-verygood.csv' WITH CSV HEADER;

COPY 21256
Time: 37588.917 ms