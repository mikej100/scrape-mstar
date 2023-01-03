Feature: Invoke scrap-morningstar with list of symbols
As investment analyst 
I want to scrape financial information from morningstar for a set of securities
So that I can use the data in my analysis programs

Scenario: Invoke crawl running in same project
Given scrapy modules are in same project as this test
And symbols dataset 1
When scrape-mstar is invoked
Then new securities_data file is created

Scenario: Invoke crawl on locally hosted scrapyd service
Given morningstar scapy module is deployed to local server
When a run request is submitted
Then the output file is produced within "10" seconds