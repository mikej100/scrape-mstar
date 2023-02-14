Feature: Create and deploy docker images for scrapy
As investment analyst 
I want to start up lastest scraping service in docker container
So that securities data can be updated for use in my analysis functions


Scenario: Create docker image for current project scrapyd
Given scrapy modules are in same project as this test
#And Docker images are managed on the current machine
When I create a new docker image 
And I deploy the docker image
