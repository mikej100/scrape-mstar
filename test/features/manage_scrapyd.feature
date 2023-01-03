Feature: Manage scrapyd
As an service operations manager
I want to manage scrapyd service
So that the scraping services can be used by higher level python scripts

Scenario: Start scrapy on local host
Given scrapyd is not running on localhost
When scapyd is started on localhost
Then scrapyd on localhost responds to a request

Scenario: Start scrapy on local host when already running
When scapyd is started on localhost
Then scrapyd on localhost responds to a request

@wip
Scenario: Deploy scrapy spider to local scrapyd server
Given scrapyd is running on localhost
And default project is not deployed on scrapyd
When default spider is deployed to localhost
Then default spider is listed by scrapyd server