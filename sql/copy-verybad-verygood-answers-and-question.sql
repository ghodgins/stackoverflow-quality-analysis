select count(*)
from (
    select id, parentid, body
    from posts
    where creationdate >= timestamp '2014-01-01 00:00:00' and
          creationdate < timestamp '2016-01-01 00:00:00' and
          posttypeid = 2 and
          lasteditdate is null
) a
join (
    select id, title, body
    from posts
    where creationdate >= timestamp '2014-01-01 00:00:00' and
          creationdate < timestamp '2016-01-01 00:00:00' and
          posttypeid = 1 and
          lasteditdate is null
) q
on (a.parentid = q.id);


COPY (
    select
        a.id as id,
        a.body as body,
        q.id as parentid,
        q.title as parenttitle,
        q.body as parentbody
    from (
        select id, parentid, body
        from posts
        where creationdate >= timestamp '2015-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 2 and
              lasteditdate is null
    ) a
    join (
        select id, title, body
        from posts
        where creationdate >= timestamp '2015-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 1 and
              lasteditdate is null
    ) q
    on (a.parentid = q.id)
) TO '/tmp/answers-extra.csv' WITH CSV HEADER;



COPY (
    select
        a.id as id,
        a.body as body,
        q.id as parentid,
        q.title as parenttitle,
        q.body as parentbody
    from (
        select id, parentid, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 2 and
              lasteditdate is null and
              score <= -2
    ) a
    join (
        select id, title, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 1 and
              lasteditdate is null
    ) q
    on (a.parentid = q.id)
    order by RANDOM()
) TO '/tmp/answers-parents-verybad.csv' WITH CSV HEADER;

COPY (
    select
        a.id as id,
        a.body as body,
        q.id as parentid,
        q.title as parenttitle,
        q.body as parentbody
    from (
        select id, parentid, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 2 and
              lasteditdate is null and
              score = -1
    ) a
    join (
        select id, title, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 1 and
              lasteditdate is null
    ) q
    on (a.parentid = q.id)
    order by RANDOM()
) TO '/tmp/answers-parents-bad.csv' WITH CSV HEADER;

COPY (
    select
        a.id as id,
        a.body as body,
        q.id as parentid,
        q.title as parenttitle,
        q.body as parentbody
    from (
        select id, parentid, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 2 and
              lasteditdate is null and
              score > 0 and
              score <= 6
    ) a
    join (
        select id, title, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 1 and
              lasteditdate is null
    ) q
    on (a.parentid = q.id)
    order by RANDOM()
) TO '/tmp/answers-parents-good.csv' WITH CSV HEADER;


COPY (
    select
        a.id as id,
        a.body as body,
        q.id as parentid,
        q.title as parenttitle,
        q.body as parentbody
    from (
        select id, parentid, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 2 and
              lasteditdate is null and
              score >= 7
    ) a
    join (
        select id, title, body
        from posts
        where creationdate >= timestamp '2014-01-01 00:00:00' and
              creationdate < timestamp '2016-01-01 00:00:00' and
              posttypeid = 1 and
              lasteditdate is null
    ) q
    on (a.parentid = q.id)
    order by RANDOM()
) TO '/tmp/answers-parents-verygood.csv' WITH CSV HEADER;

# Answers Very Bad
COPY 4958

# Answers Bad
COPY 25655

# Answers Good
COPY 974005

# Answers Very Good
COPY 21256
