#! /bin/bash

projPath = "C:\Users\User\Mike Jennings\Investment club - General\analysis\20210714_morningstar_data"

cd projPath
 .\venv\Scripts\activate

 scrapy crawl funds3 -O ..\..\..\data\analysis\funds3.json
# scrapy crawl funds2 -O ..\..\..\data\analysis\funds2.json" 
# scrapy crawl funds1 -O ..\..\..\data\analysis\funds1.json 