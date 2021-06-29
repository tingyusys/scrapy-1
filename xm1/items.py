# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Xm1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    two_url = scrapy.Field()
    title = scrapy.Field()
    media_types = scrapy.Field()
    digests = scrapy.Field()
    time = scrapy.Field()
    picture = scrapy.Field()
    content = scrapy.Field()

