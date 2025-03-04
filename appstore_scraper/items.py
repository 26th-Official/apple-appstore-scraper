# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class App(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    user_rating = scrapy.Field()
    developer = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()