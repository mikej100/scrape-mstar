Feature: Manage scrapyd
As an service operations manager
I want to manage scrapyd service
So that the scraping services can be used by higher level python script

@test_start @wip
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

Scenario: Stop already running scrapyd
Given scrapyd is running on localhost
When scrapyd service is stopped on localhost
Then scrapyd is not running on localhost

@stop_scrapyd
Scenario: Stop scrapyd
When scrapyd service is stopped on localhost
Then scrapyd is not running on localhost

@fast @fast2 @start_scrapyd
Scenario: Run scrapy-start-deploy-crawl-stop
Given scrapyd is not running on localhost
And symbols dataset 2 comprising one fund
When scrapyd start and deploy script is run
And scrape-mstar is invoked
Then "3" new documents are created in MongoDB Atlas database