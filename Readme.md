Financial data webscraping service
==================================

scrape-mstar scrapes data from financial information
web pages on financial securities for use by a
separate portfolio holdings analysis application (holdings_ana).

The application is under development.

The service is invoked by sending a request to the scrapyd service with a list
of symbols and types of securities. The symbols for each security are defined
for the financial information service used for the web lookup.

The scrapyd service requests pages on the financial services website
and retrieve information from three sub-pages: 
summary, performance and risk. Security types covered are stocks and different types of 
fund. Data retrieved includes market price, date, currency,
 regions, sectors, trailing returns, Sharpe, beta and alpha performance measures. 
 The data is written to MongoDB database so that it can be queried by 
 the securities holdings analysis application.

 Installation
===============

## Set up venv environment management
### One time set up
In the project root, create .venv here, activate and verify is active
    sudo apt install python3.12-venv
    python3 -m venv .venv
    source .venv/bin/activate
    which python


    pip install -r requirements.txt
    sudo apt-get install libxml2-dev libxslt-dev
    pip install git+https://github.com/scrapy/scrapyd-client.git
    pip install playwright
    
    playwright install

### Configure MongoDB connection
Set envrionment variable MONGO_CONN_STRING=<mongodb-connectionstring>. 
You may want to do this in .bashrc or VScode project settings.

To run 
-----
in the home directory, on the command line enter

    source .venv/bin/activate
    scrapyd

Or run the behave test "Deploy scrapy spider to local scrapyd server" using the
VS Code test explorer and running in debug mode (it fails running not in debug)

Troubleshooting
---------------
### Failure to submit job to scrapyd
Steps to produce: submit a crawl job to scheduled on  scrapyd server.

Expected result: Return a run_id for the job.

Observed result: Submission request complets with 200 http request status, but 
response status is "error" and end of error message includes 
"KeyError: 'MONGO_CONN_STRING'". Look in log.txt file.

Cause: environment variable MONGO_CONN_STRING not set, or set to wrong or out 
out of date password value.

Remedy: Set environmnet variable is to valid connection string in the environment in which scrapyd 
was started. For example, check .bashrc includes lines to set the value, and that the value is correct according to configuration in admin in mondodb.com.

Development
-----------
To support the development lifecycle, the following capabilities are supported
- invoke the scrapy run from the development environment; for screen scraping code
development
- deploy the scrapy capability to scrapyd to run as a service, to start and stop
the service, and to schedule scraping runs on the service. To test the service and
for it to be used by the analysis application running on the same host
- deploy the scrapyd service to Docker container, to start and stop the container and
to invoke the scraping service. To to test the container deployment and to deploy the
service as a cloud-hosted service in the future.  The container is configured currently
 to run on the host machine.

The service runs on Linux platform. This is necessary because the Playwright 
scraping library which is required to handle certain types of security is not 
supported on Windows.  Hence the need to run the scraper as a web service. 

This is a development project. The configuration for VS Code, Behave and pytest
features are included in the repository. Some of these will contain local 
implementation details.

Packages used in construction
Web scraping: scrapy, scrapyd, playwright
Deployment: Docker container, MongoDB Atlas cloud-hosted database
Testing: Behave, pytest
IDE: VS Code (some vs-specific debug configurations are included in the repo)


### Run in VS Code

To run the scraping service in various modes refer to the corresponding tests in 
the Behave feature files or pytest or the instructions below.

The project is set up to run code from tests: mostly Behave tests, and also
some pytests for development phase. In production it is expected to be run as a 
service in a container.

Option 1. Install VS Code extension "Behave VSC". With this you can run 
individual scenarios
or features from the Test Explore or from the feature files, with option to run
in debug

Option 2. Run from VS Code "Run and Debug" panel, using
- Behave current file: will run current feature fle
- wipBehave: will run scenarios tagged with "wip"

The behave tests cover:
- scrapy running locally as part of the project
- deploying scrapy to scrapyd and scheduling jobs 
- deploying to local Docker container and scheduling jobs

Retained tests are for writing output to Mongodb. Tests which are commented out
cover testing writing to local files, but this feature is not currently
utilised.

### Deploy to scrapyd locally
`scrapyd`   to start server
`scrapyd-deploy`

To confirm server is running and list project deployed:
`curl http://localhost:6800/listprojects.json`

### Docker
`docker build --tag scrape-mstar .`
`docker compose up`

To run behave tests which shutdown the local scrapyd service the following line 
needs to be written to a file in /etc/sudoers.d/
<admin-account-name> ALL=(ALL:ALL) NOPASSWD: /usr/bin/killall
