import scrapy

from selenium import webdriver
from selenium.webdriver import Chrome
from  selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import scrapy

class TanyanchaSpider(scrapy.Spider):
    name = "tanyancha"
    start_urls = ["https://www.tianyancha.com"]

    # 实例化一个浏览器对象
    def __init__(self):
        self.driver = webdriver.Chrome()
        super().__init__()

    def parse(self,response):
        url = self.start_urls[0]
        response = scrapy.Request(url, callback=self.parse_main)
        yield response

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        self.driver.quit()



    # 访问主页的url, 拿到对应板块的response
    def parse_main(self, response):
        div_list = response.xpath("//div[@class='ns_area list']/ul/li/a/@href").extract()
        index_list = [3,4,6,7]
        for index in index_list:
            response = scrapy.Request(div_list[index],callback=self.parse_detail)
            yield response