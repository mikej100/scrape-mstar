Feature: Foreign Exchange currency conversion service
As a developer of financial analysis applications
I want a currency conversion service
So that I can use currency conversions in python, R and excel applications

Scenario: Date conversions between POSIX and Trading Academy data
When integer "1674259200" representing the date 2023-01-21 for conversion
Then the result is "12124800"

@wip
Scenario: Python function to convert USD to GBP
Given a MongoDB Atlas cloud database with historic GBPUSD exchange rates
When the python conversion function is called with date "2020-09-23"
Then the conversion rate is "1.21"