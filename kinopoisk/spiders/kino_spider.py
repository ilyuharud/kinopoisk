from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from kinopoisk.items import KinoposkItemLoader, KinopoiskItem

class KinoSpider(CrawlSpider):
    name = 'kino_spider'
    allowed_domains = ['www.kinopoisk.ru']
    start_urls = [
        u'https://www.kinopoisk.ru/film/326'
    ]

    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths=['//div[contains(@class, "feature_film_header")]/h1/text()'],
                allow = r'https://www.kinopoisk.ru/film/\d+$'
            ),
            callback = 'parse_item'
        )
    ]

    def pase_item(self, response):
        selector = Selector(response, 'utf-8')
        l = KinoposkItemLoader(KinopoiskItem, selector)
        l.add_xpath('url', response.url)
        l.add_xpath('name', '//div[contains(@class, "feature_film_header")]/h1/text()')
        l.add_xpath('description', '//div[contains(@itemprop, "description")]/text()')
        l.add_xpath('genre', '//span[contains(@itemprop, "genre")]//a/text()')
        l.add_xpath('year', '//table[@class="info"]/tbody[1]/tr[1]/td[2]/div[1]/a/text()')
        l.add_xpath('actors', '//div[@id="actorList"]/ul[1]/li/a/text()')
        l.add_xpath('directors', '//tr[4]/td/a/text()')