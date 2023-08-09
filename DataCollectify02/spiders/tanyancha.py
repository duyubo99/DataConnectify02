import scrapy

# python -m scrapy genspider tanyancha www.tianyancha.com
class TanyanchaSpider(scrapy.Spider):
    name = "tanyancha"
    start_urls = ["https://www.tianyancha.com"]

    def parse(self, response):

        pass
