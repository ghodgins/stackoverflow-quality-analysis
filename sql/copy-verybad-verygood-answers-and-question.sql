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
        a.id as answerid,
        a.body as answerbody,
        q.id as questionid,
        q.title as questiontitle,
        q.body as questionbody
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