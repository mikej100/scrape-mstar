# Holdings data file does not need to be read, so tests are obsolete
# The holdings file is read by holdings-ana.
@skip
Feature: Read holdings and funds base data from excel file
As an investor
I want my holdings data to be read from an excel file
So that I can maintain the data conveniently for analysis

Scenario: Read funds base data
Given investment book file in financial analysis folder
When the workbook is read
Then the number of FundsBase entries is "37" 