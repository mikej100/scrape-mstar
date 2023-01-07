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

pip install scrapy\
            scrapy-playwright\
            behave PyHamcrest\
            scrapyd\
            python-scrapyd-api
pip install git+https://github.com/scrapy/scrapyd-client.git
playwright install


Activate "Select and Run" Activity.
From the run drop-down (green triangle), select "Crawl with funds1"

Run as service on localhost
--------------------------
To start the service on localhost run scrapy_manager.py. When run as a script, this will 
start the scrapyd server and deploy the project and spider.

To run behave tests which shutdown the local scrapyd service the following line 
needs to be written to a file in /etc/sudoers.d/
<admin-account-name> ALL=(ALL:ALL) NOPASSWD: /usr/bin/killall