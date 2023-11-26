import scrapy


class SkimsSpider(scrapy.Spider):
    name = "skims"
    allowed_domains = ["skims.com"]
    start_urls = ["https://skims.com/"]

    def parse(self, response):
        pass
