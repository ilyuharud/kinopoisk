# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

class KinopoiskItem(Item):
    url = Field()
    name = Field()
    description = Field()
    genre = Field()
    year = Field()
    actors = Field()
    director = Field()

class KinoposkItemLoader(ItemLoader):
    url_out = TakeFirst()
    name_out = TakeFirst()
    description_out = TakeFirst()
    genre_out = Join(separator=',')
    year_out = TakeFirst()
    actors_out = Join(separator=',')
    director_out = Join(separator=',')