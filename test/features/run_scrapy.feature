Feature: Invoke scrap-morningstar with list of symbols
As investment analyst 
I want to scrape financial information from morningstar for a set of securities
So that I can use the data in my analysis programs

@deploy
Scenario: Run crawl in same project for all security types
Given scrapy modules are in same project as this test
And symbols dataset 1 comprising one each of fund, cef and equity
When scrape-mstar is invoked
Then "5" new documents are created in MongoDB Atlas database

Scenario: Invoke crawl on locally hosted scrapyd service writing to local file
Given default scrapy project is deployed to local server
When a small job is submitted
Then the output file is produced within "10" seconds

@fast @wip @fast1
Scenario: Invoke crawl running in same project and write to MongoDB
Given scrapy modules are in same project as this test
#And symbols dataset 1 comprising one each of fund, cef and equity
And symbols dataset 2 comprising one fund
When scrape-mstar is invoked
Then "3" new documents are created in MongoDB Atlas database

Scenario: Invoke crawl running in same project and write to MongoDB
Given scrapy modules are in same project as this test
#And symbols dataset 1 comprising one each of fund, cef and equity
And symbols file "test_5_funds.json"
When scrape-mstar is invoked
Then "5" new documents are created in MongoDB Atlas database