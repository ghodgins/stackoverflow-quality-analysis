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