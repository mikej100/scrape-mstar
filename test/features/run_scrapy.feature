Feature: Invoke scrap-morningstar with list of symbols
As scrape-morningstar developer  
I want to scrape financial information from morningstar for a set of securities
So that I can develop scraping facility to provide securities data for holdings analysis

@fast #@wip @fast1
Scenario: Invoke one fund crawl running in same project, write to MongoDB
Given scrapy modules are in same project as this test
And security type is "fund" and morningstar symbol is "F000013G37"
When scrape-mstar is invoked
Then "3" new documents are created in MongoDB Atlas database

Scenario: Invoke one etf crawl running in same project, write to MongoDB
Given scrapy modules are in same project as this test
And security type is "etf" and morningstar symbol is "0P0001HZ0W"
When scrape-mstar is invoked
Then "3" new documents are created in MongoDB Atlas database



Scenario: Run crawl for each type in same project, write to mongo
Given scrapy modules are in same project as this test
And symbols dataset 1 comprising one each of fund, cef and equity
When scrape-mstar is invoked
Then "7" new documents are created in MongoDB Atlas database

# Scenario: Invoke crawl on locally hosted scrapyd service writing to local file
# Given default scrapy project is deployed to local server
# When a small job is submitted
# Then the output file is produced within "10" seconds
