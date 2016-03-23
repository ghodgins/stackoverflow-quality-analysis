Correlation between viewcount and score:
select corr(viewcount, score) from posts where creationdate >= timestamp '2015-01-01 00:00:00' and creationdate < timestamp '2016-01-01 00:00:00';
 0.43960496811704