import scrapy


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
        self.log(f'response url {response.url}')
        fundId = response.url.split("?")[1]
        filename = f'funds-{fundId}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')