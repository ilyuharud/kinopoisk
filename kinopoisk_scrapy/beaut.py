import requests
from bs4 import BeautifulSoup
import csv
import time
import re


def get_html(url, session):
    headers = {"Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.8"}
    r = session.get(url, headers=headers, timeout=(360, 360))
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = pages.split('=')[1].split('&')[0]
    except:
        total_pages = '1'
    return int(total_pages)


def write_csv(data):
    with open('C:/Users/aandryushina/Documents/avito_new.csv', 'a', encoding='cp1251', newline='') as f:
        writer = csv.writer(f)
        try:
            writer.writerow((
                            data['rooms'], data['floor'], data['house'], data['square'], data['price'], data['address'],
                            data['lat'], data['lon']))
        except:
            print("Wrong data format")


def get_pages_url(html):
    soup = BeautifulSoup(html, 'lxml')
    adf = soup.find('div', class_='catalog-list')

    if adf is None:
        print("Page format is wrong")
    else:
        ads = adf.find_all('div', class_='item_list')
        for ad in ads:
            time.sleep(2)
            try:
                url = 'https://www.avito.ru' + ad.find('div', class_="title description-title").find('h3').find(
                    'a').get('href')
            except:
                url = ''
            d = get_pages_data(get_html(url, session))
            write_csv(d)


def get_pages_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        cnt_params = len(soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item'))
    except:
        cnt_params = 0
    for i in range(0, cnt_params):
        if soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(':')[
            0].strip() == 'Количество комнат':
            try:
                rooms = \
                soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(
                    ':')[1].split('-')[0].strip().replace(u'\xb2', ' ').replace(u'\u261d', ' ')
            except:
                rooms = ''

        if soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(':')[
            0].strip() == 'Этаж':
            try:
                floor = \
                soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(
                    ':')[1].strip().replace(u'\xb2', ' ').replace(u'\u261d', ' ')
            except:
                floor = ''

        if soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(':')[
            0].strip() == 'Этажей в доме':
            try:
                house = \
                soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(
                    ':')[1].strip().replace(u'\xb2', ' ').replace(u'\u261d', ' ')
            except:
                house = ''

        if soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(' ')[
            0].strip() == 'Общая':
            try:
                square = \
                soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')[i].text.split(
                    ' ')[2].strip().split('\xa0м?')[0].replace(u'\xa0', ' ').replace(u'\u261d', ' ').replace(u'\xb2',
                                                                                                             ' ').split(
                    ' м')[0]
            except:
                square = ''

    try:
        price = soup.find('div', class_='price-value').find_all('span', class_='js-item-price')[0].text.replace(u'\xb2',
                                                                                                                ' ').replace(
            u'\u261d', ' ').replace(' ', '')
    except:
        price = ''
    try:
        address = soup.find('span', class_='item-map-address').text.strip().replace(u'\xb2', ' ').replace(u'\n',
                                                                                                          ' ').replace(
            u'\u261d', ' ').replace('  ', ' ')
    except:
        address = ''
    try:
        lat = soup.find('div', "b-search-map").attrs['data-map-lat']
    except:
        lat = ''
    try:
        lon = soup.find('div', "b-search-map").attrs['data-map-lon']
    except:
        lon = ''

    data = {'rooms': rooms,
            'floor': floor,
            'house': house,
            'square': square,
            'price': price,
            'address': address,
            'lat': lat,
            'lon': lon
            }
    return data


def getLinks(pageUrl, type_rooms):
    url_main = "https://www.avito.ru"
    url = url_main + "/" + pageUrl + "/kvartiry/prodam/" + type_rooms
    page_part = 'p='
    view_part = 'view=list'
    user_part = '&user='
    type_flat = ["/vtorichka", "/novostroyka"]
    # "/vtorichka","/novostroyka"

    for type_f in type_flat:
        for i in range(1, 3):
            # , 3
            time.sleep(2)
            url_view = url + type_f + '?' + view_part + user_part + str(i)
            html_user = get_html(url_view, session)
            pages_cnt = get_total_pages(html_user)
            for j in range(1, pages_cnt + 1):
                try:
                    time.sleep(2)
                    url_p = url + type_f + '?' + page_part + str(j) + user_part + str(i) + '&' + view_part
                    print(url_p)
                    html_p = get_html(url_p, session)
                    get_pages_url(html_p)
                except:
                    print("page not found")


def main():
    regions = ["moskva", "moskovskaya_oblast", "sankt-peterburg", "leningradskaya_oblast", "adygeya", "altayskiy_kray",
               "amurskaya_oblast", "arhangelskaya_oblast", "astrahanskaya_oblast", "bashkortostan",
               "belgorodskaya_oblast", "bryanskaya_oblast", "buryatiya", "vladimirskaya_oblast",
               "volgogradskaya_oblast", "vologodskaya_oblast", "voronezhskaya_oblast", "dagestan", "evreyskaya_ao",
               "zabaykalskiy_kray", "ivanovskaya_oblast", "ingushetiya", "irkutskaya_oblast", "kabardino-balkariya",
               "kaliningradskaya_oblast", "kalmykiya", "kaluzhskaya_oblast", "kamchatskiy_kray",
               "karachaevo-cherkesiya", "kareliya", "kemerovskaya_oblast", "kirovskaya_oblast", "komi",
               "kostromskaya_oblast", "krasnodarskiy_kray", "krasnoyarskiy_kray", "respublika_krym",
               "kurganskaya_oblast", "kurskaya_oblast", "lipetskaya_oblast", "magadanskaya_oblast", "mariy_el",
               "mordoviya", "murmanskaya_oblast", "nenetskiy_ao", "nizhegorodskaya_oblast", "novgorodskaya_oblast",
               "novosibirskaya_oblast", "omskaya_oblast", "orenburgskaya_oblast", "orlovskaya_oblast",
               "penzenskaya_oblast", "permskiy_kray", "primorskiy_kray", "pskovskaya_oblast", "respublika_altay",
               "rostovskaya_oblast", "ryazanskaya_oblast", "samarskaya_oblast", "saratovskaya_oblast",
               "sahalinskaya_oblast", "saha_yakutiya", "sverdlovskaya_oblast", "severnaya_osetiya",
               "smolenskaya_oblast", "stavropolskiy_kray", "tambovskaya_oblast", "tatarstan", "tverskaya_oblast",
               "tomskaya_oblast", "tulskaya_oblast", "tyva", "tyumenskaya_oblast", "udmurtiya", "ulyanovskaya_oblast",
               "habarovskiy_kray", "hakasiya", "hanty-mansiyskiy_ao", "chelyabinskaya_oblast",
               "chechenskaya_respublika", "chuvashiya", "chukotskiy_ao", "yamalo-nenetskiy_ao", "yaroslavskaya_oblast"]
    # ,
    global session
    session = requests.Session()

    url_main = "https://www.avito.ru"
    page_part = 'p='
    view_part = 'view=list'
    user_part = '&user='
    rooms = ["6-komnatnye", "7-komnatnye", "8-komnatnye", "9-komnatnye", "mnogokomnatnye"]

    #     url_view_t_v = url_main+"/"+ "chuvashiya"+ "/kvartiry/prodam/2-komnatnye" + "/vtorichka" + '?' + view_part  + user_part + str(1)
    #     html_user=get_html(url_view_t_v,session)
    #     pages_cnt=get_total_pages(html_user)
    #     for j in range( 9,pages_cnt+1):
    #         time.sleep(2)
    #         url_p= url_main+"/"+ "chuvashiya"+ "/kvartiry/prodam/2-komnatnye"  + "/vtorichka"  + '?'+ page_part+ str(j) +user_part+ str(1) +'&'+view_part
    #         print(url_p)
    #         html_p=get_html(url_p,session)
    #         get_pages_url(html_p)

    #     for i in range(1,3):
    #         time.sleep(2)
    #         url_view_n =url_main+"/"+ "chuvashiya"+ "/kvartiry/prodam/2-komnatnye" + "/novostroyka" + '?' + view_part  + user_part + str(i)
    #         html_user=get_html(url_view_n,session)
    #         pages_cnt=get_total_pages(html_user)
    #         for j in range(1,pages_cnt+1):
    #             time.sleep(2)
    #             url_p= url_main+"/"+ "chuvashiya"+ "/kvartiry/prodam/2-komnatnye"  + "/novostroyka"  + '?'+ page_part+ str(j) +user_part+ str(i) +'&'+view_part
    #             print(url_p)
    #             html_p=get_html(url_p,session)
    #             get_pages_url(html_p)
    for type_rooms in rooms:
        for reg in regions:
            getLinks(reg, type_rooms)


#         #/sverdlovskaya_oblast/kvartiry/prodam/1-komnatnye


if __name__ == '__main__':
    main()