import scrapy
from scrapy.spiders import SitemapSpider
import json

from appstore_scraper.items import App


class AppsSpider(SitemapSpider):
    name = "apps"
    allowed_domains = ["apps.apple.com"]
    sitemap_urls = [
        'https://apps.apple.com/sitemaps_apps_index_app_1.xml',
    ]
    sitemap_rules = [
        ('/us/', 'parse'),
    ]

    def parse(self, response):
        script = response.xpath('//script[@id="shoebox-media-api-cache-apps"]/text()').get()
        raw_data = json.loads(script)
        key_0 = list(raw_data.keys())[0]
        data = json.loads(raw_data[key_0])['d'][0]

        yield App(
            {
                'name': data['attributes']['name'],
                'user_rating': data['attributes']['userRating'],
                'developer': data['relationships']['developer'],
                'price': data['attributes']['platformAttributes']['ios']['offers'][0]['price'],
            }
        )


