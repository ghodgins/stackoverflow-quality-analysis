select extract(month from creationdate), count(*)
from posts
where
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00' and
    posttypeid = 1
group by extract(month from creationdate);