# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

class KinopoiskItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    year = scrapy.Field()
    actors = scrapy.Field()
    director = scrapy.Field()

class KinoposkItemLoader(ItemLoader):
    url_out = TakeFirst()
    name_out = TakeFirst()
    description_out = TakeFirst()
    genre_in = Join()
    genre_out = TakeFirst()
    actors_in = Join()
    actors_out = TakeFirst()
    director_out = TakeFirst()