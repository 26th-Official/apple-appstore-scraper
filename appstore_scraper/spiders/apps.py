import scrapy


class AppsSpider(scrapy.Spider):
    name = "apps"
    allowed_domains = ["apps.apple.com"]
    start_urls = ["https://apps.apple.com"]

    def parse(self, response):
        pass
