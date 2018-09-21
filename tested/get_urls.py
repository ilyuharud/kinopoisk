import requests
from lxml import html

file = open('input/part-1.csv', "w")


def get_link(id):
    return 'https://www.kinopoisk.ru/top/lists/322/filtr/all/sort/votes/page/%s/' % id


def parse_page(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree.xpath("//a[@class='all']/@href")


for id in range(1, 195):
    url = get_link(id)
    print(url)
    links = parse_page(url)
    for link in list(links):
        if (str(link).__contains__('film')):
            file.write(str(link) + "\n")

file.close()
