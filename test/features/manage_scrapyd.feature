Feature: Manage scrapyd
As an service operations manager
I want to manage scrapyd service
So that the scraping services can be used by higher level python script

@start @wip
Scenario: Start scrapy on local host
Given scrapyd is not running on localhost
When scapyd is started on localhost
Then scrapyd on localhost responds to a request

Scenario: Start scrapy on local host when already running
When scapyd is started on localhost
Then scrapyd on localhost responds to a request

Scenario: Deploy scrapy spider to local scrapyd server
Given scrapyd is running on localhost
And default project is not deployed on scrapyd
When default project is deployed to localhost
Then default project is listed by scrapyd server

Scenario: Stop and restart scrapyd
Given scrapyd is running on localhost
When scrapyd service is stopped on localhost
Then scrapyd is not running on localhost

@wip
Scenario: Run scrapy-start-deploy script and crawl
Given scrapyd is not running on localhost
When scrapyd start and deploy script is run
And a small job is submitted
Then the output file is produced within "10" seconds