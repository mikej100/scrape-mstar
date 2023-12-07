Financial data webscraping service
==================================

scrape-mstar is used to scrape financial data from financial information
web pages.

The service is under development and not suitable for others to use, yet.

The full service runs on Linux platform only. This is due to one of the 
web page scraping components not working on Windows. The package concerned is 
Playwright and it may become useable on Windows in the future. The forex python
script can be run on Windows.

The service runs as a web service by scrapyd. scrapyd can run as a local
service, and on a Docker container. The suite includes scripts to build and run
the container, on local machine currently.

Results are written to local files in the project structure. The design is to 
write results to MongoDB Atlas database.

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

Running the spider scrapers
===========================

Check the investments workbook is not open in Excel.


In vsCode
---------
### Switch to required version of Python
In Terminal enter
    .\venv\Scripts\activate

### Check configuration
Name of the investments workbook

### Installation
pip install requirements.txt
pip install git+https://github.com/scrapy/scrapyd-client.git
playwright install

### Configure MongoDB connection
Set envrionment variable MONGO_CONN_STRING=<mongodb-connectionstring>. You may want to do this in .bashrc or VScode project settings.


### Run in VS Code
To run in debug 
    launch "wipBehave" will run scenarios tagged with @wip
    launch Behave: current file (feature file)
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