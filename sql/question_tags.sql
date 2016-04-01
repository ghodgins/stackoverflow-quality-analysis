select count(*) from posts where tags is null;
  count
----------
 17726562
(1 row)

Time: 39328.243 ms
select count(*) from posts where tags is not null;
  count
----------
 10789363
(1 row)

Time: 41488.903 ms

select tags, count(*)
from posts
where
    tags ~ '^<[^<>]+>$' and
    creationdate >= timestamp '2015-01-01 00:00:00' and
    creationdate < timestamp '2016-01-01 00:00:00'
group by tags
order by count(*) desc
limit 100;


         tags         | count
----------------------+-------
 <android>            | 15431
 <java>               | 14428
 <javascript>         | 12303
 <php>                | 10738
 <python>             | 10698
 <r>                  |  7795
 <mysql>              |  7519
 <c#>                 |  7494
 <c++>                |  7243
 <angularjs>          |  6741
 <jquery>             |  5805
 <c>                  |  4530
 <ruby-on-rails>      |  3193
 <css>                |  2653
 <sql-server>         |  2550
 <matlab>             |  2536
 <git>                |  2427
 <vb.net>             |  2317
 <swift>              |  2148
 <ruby>               |  2057
 <elasticsearch>      |  1909
 <ios>                |  1899
 <regex>              |  1798
 <sql>                |  1772
 <powershell>         |  1598
 <scala>              |  1587
 <wordpress>          |  1520
 <mongodb>            |  1507
 <excel>              |  1485
 <go>                 |  1297
 <node.js>            |  1282
 <meteor>             |  1231
 <bash>               |  1230
 <html>               |  1214
 <haskell>            |  1208
 <excel-vba>          |  1198
 <perl>               |  1171
 <batch-file>         |  1140
 <magento>            |  1130
 <asp.net>            |  1088
 <postgresql>         |  1000
 <rust>               |   916
 <django>             |   900
 <asp.net-mvc>        |   865
 <ember.js>           |   857
 <vim>                |   812
 <docker>             |   755
 <objective-c>        |   713
 <reactjs>            |   708
 <python-2.7>         |   696
 <google-apps-script> |   688
 <oracle>             |   670
 <sas>                |   668
 <python-3.x>         |   609
 <algorithm>          |   594
 <parse.com>          |   586
 <twitter-bootstrap>  |   583
 <unity3d>            |   567
 <symfony2>           |   567
 <d3.js>              |   566
 <.htaccess>          |   548
 <apache-spark>       |   519
 <vba>                |   503
 <grails>             |   503
 <react-native>       |   502
 <highcharts>         |   500
 <nginx>              |   486
 <linux>              |   483
 <android-studio>     |   480
 <prolog>             |   477
 <neo4j>              |   469
 <vbscript>           |   460
 <jmeter>             |   449
 <hadoop>             |   445
 <google-analytics>   |   440
 <typescript>         |   438
 <jenkins>            |   437
 <sql-server-2008>    |   435
 <three.js>           |   433
 <clojure>            |   426
 <delphi>             |   426
 <eclipse>            |   426
 <ms-access>          |   426
 <maven>              |   425
 <xcode>              |   423
 <wpf>                |   413
 <f#>                 |   410
 <google-bigquery>    |   405
 <google-spreadsheet> |   395
 <solr>               |   392
 <codeigniter>        |   381
 <shell>              |   366
 <azure>              |   366
 <spring>             |   362
 <actionscript-3>     |   352
 <polymer>            |   352
 <laravel>            |   350
 <paypal>             |   349
 <ruby-on-rails-4>    |   346
 <qt>                 |   342
(100 rows)
