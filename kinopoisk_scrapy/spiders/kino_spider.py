from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from kinopoisk_scrapy.items import KinopoiskItem, KinoposkItemLoader

class KinoSpider(CrawlSpider):
    name = 'kinopoisk_scrapy'
    allowed_domains = ['www.kinopoisk_scrapy.ru']
    start_urls = ['https://www.kinopoisk_scrapy.ru/film/326']

    rules = (Rule(LinkExtractor(allow=r'https://www.kinopoisk_scrapy.ru/film/\d+'), callback='parse_item'),)

    def parse_item(self, response):
        loader = KinoposkItemLoader(item=KinopoiskItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', '//div[contains(@class, "feature_film_header")]/h1/text()')
        loader.add_xpath('description', '//div[contains(@itemprop, "description")]/text()')
        loader.add_xpath('genre', '//span[contains(@itemprop, "genre")]//a/text()')
        loader.add_xpath('year', '//table[@class="info"]/tbody[1]/tr[1]/td[2]/div[1]/a/text()')
        loader.add_xpath('actors', '//div[@id="actorList"]/ul[1]/li/a/text()')
        loader.add_xpath('director', '//tr[4]/td/a/text()')
        return loader.load_item()