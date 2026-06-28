
create database Web_scraping;

use Web_scraping;

select distinct(Page_Title) from Pageviews;

update Pageviews
set Page_Title = REPLACE(Page_Title,'_',' ');

delete from Pageviews where Page_Title in ('Main Page', 'Special:Search');

select distinct(Page_Title) from Pageviews;

select Page_Title, MAX(Number_of_Visits) [Max Views], AVG(Number_of_Visits) [Avg Views] from Pageviews group by Page_Title order by [Max Views] desc;
