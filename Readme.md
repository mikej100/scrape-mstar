Financial data webscraping service
==================================

scrape-mstar scrapes data from financial information
web pages on financial securities for use by a
separate portfolio holdings analysis application(holdings_ana).

The application is under development.

The service is invoked by sending an http request to the scrapyd service.
The body of the request is json which specifies the symbols and type of the 
securities for which financial data is required. 

The scrapyd service requests pages on the financial services website
for each of the securities specified and retrieve information from three sub-pages: 
summary, performance and risk. Security types covered are stocks and different types of 
fund. Data retrieved includes market price, date, currency,
 regions, sectors, trailing returns, Sharpe, beta and alpha performance measures. 
 The data is written to MongoDB database so that it can be queried by 
 the securities holdings analysis application.

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

Foreign exchange function is included in the suite. This uses a set of historic 
GPB-USD exchange rates hosted on the project-specific MongoDB Atlas database.

This is a development project. The configuration for VS Code, Behave and pytest
features are included in the repository. Some of these will contain local 
implementation details.

Packages used in construction
Web scraping: scrapy, scrapyd, playwright
Deployment: Docker container, MongoDB Atlas cloud-hosted database
Testing: Behave, pytest
IDE: VS Code (some vs-specific debug configurations are included in the repo)

To run the scraping service in various modes refer to the corresponding tests in 
the Behave feature files or pytest or the instructions below.

### Installation
pip install requirements.txt
pip install git+https://github.com/scrapy/scrapyd-client.git
playwright install

### Configure MongoDB connection
Set envrionment variable MONGO_CONN_STRING=<mongodb-connectionstring>. 
You may want to do this in .bashrc or VScode project settings.


### Run in VS Code
To run in debug 
    launch "wipBehave" to run scenarios tagged with @wip
    launch Behave: to run current file feature file
    launch allSecSpiders or CrawlFunds1

### Deploy to scrapyd
`scrapyd`   to start server
`scrapy-deploy`

or run `scrapy-start-deploy` script.

To confirm server is running and list project deployed:
`curl http://localhost:6800/listprojects.json`

### Docker
`docker build --tag scrape-mstar .`
`docker compose up`


Activate "Select and Run" Activity.
From the run drop-down (green triangle), select "Crawl with funds1"

Run as service on localhost
--------------------------
To start the service on localhost run scrapy_manager.py. When run as a script, this will 
start the scrapyd server and deploy the project and spider.

To run behave tests which shutdown the local scrapyd service the following line 
needs to be written to a file in /etc/sudoers.d/
<admin-account-name> ALL=(ALL:ALL) NOPASSWD: /usr/bin/killall

Run in local Docker container
-----------------------
docker build --tag scrape-mstar .
docker compose up

Service is accessible on \\localhost:6800