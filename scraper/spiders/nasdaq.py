import scrapy


class NasdaqSpider(scrapy.Spider):
    name = 'nasdaq'
    allowed_domains = ['nasdaq.com']
    start_urls = ['http://nasdaq.com/']

    def parse(self, response):
        pass
