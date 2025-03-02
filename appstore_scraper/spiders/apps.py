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
    
    def __init__(self, output_file='apps.json', output_format='json', *args, **kwargs):
        """Initialize the spider with output file and format parameters."""
        super(AppsSpider, self).__init__(*args, **kwargs)
        self.output_file = output_file
        self.output_format = output_format
        
        # Set the feed export settings
        self.custom_settings = {
            'FEEDS': {
                output_file: {
                    'format': output_format,
                    'encoding': 'utf8',
                    'store_empty': False,
                    'overwrite': False,  # Append to existing file if resuming
                }
            }
        }
        
        self.logger.info(f"Spider initialized with output file: {output_file}, format: {output_format}")

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


