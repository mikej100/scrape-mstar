import scrapy
import re


class Funds1Spider(scrapy.Spider):
    name = "funds1"

    def start_requests(self):
        fundIds = [
            "F0000103JP",
            "F0GBR04SAT"
        ]
        urlStem = 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='

        for fundId in fundIds:
            yield scrapy.Request(url=urlStem + fundId, callback=self.parse)

    def parse(self, response):
        isinText = response.xpath("//td[contains(.,'ISIN')]/following-sibling::*/text()").getall()[1]
        priceText =  response.xpath("//td[contains(.,'NAV')]/following-sibling::*/text()").getall()[1]
        yield {
            "isin" : isinText,
            "currency" : re.search("^.{3}", priceText).group(),
            "price": re.search(r"[0-9]+\.?[0-9]+",priceText).group()
        }
