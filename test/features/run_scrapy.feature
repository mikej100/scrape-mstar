Feature: Invoke scrap-morningstar with list of symbols
As investment analyst 
I want to scrape financial information from morningstar for a set of securities
So that I can use the data in my analysis programs

Scenario: Invoke crawl running in same project
Given scrapy modules are in same project as this test
And symbols dataset 1 comprising one each of fund, cef and equity
When scrape-mstar is invoked
Then new securities_data file is created

Scenario: Invoke crawl on locally hosted scrapyd service writing to local file
Given default scrapy project is deployed to local server
When a small job is submitted
Then the output file is produced within "10" seconds

@wip
Scenario: Invoke crawl running in same project and write to MongoDB
Given scrapy modules are in same project as this test
#And symbols dataset 1 comprising one each of fund, cef and equity
And symbols dataset 2 comprising one fund
When scrape-mstar is invoked
Then "3" new documents are created in MongoDB Atlas database