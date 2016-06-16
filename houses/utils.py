# coding=utf-8
import re
import requests
import urllib
import unidecode
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from django.contrib.gis.geos import GEOSGeometry

from models import House

from django.template import Context, loader
from hendrix.contrib.async.messaging import hxdispatcher

# TODO: move to settings?
# remove object url
# "/mijn/objectactions/removesavedobject/?internalId=21026942-0638-4b06-ac6c-c8d868732925&amp;tinyId=49694610"
BEWRD_URL = 'http://www.funda.nl/mijn/bewaard/'
LOGIN_URL = 'https://www.funda.nl/mijn/login'
GEOCODE_URL = 'https://geodata.nationaalgeoregister.nl/geocoder/Geocoder?zoekterm='


def scrape_funda(username, password):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'})
    tokenRequest = session.get('https://www.funda.nl/mijn/login/')

    request_validation_re = re.compile(r'<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />')
    tokens = request_validation_re.findall(tokenRequest.text)

    sessionCookies = tokenRequest.cookies

    payload = {
        '__RequestVerificationToken': tokens[0],
        'Username': username,
        'Password': password,
        'RememberMe': 'false'
    }

    raw = urllib.urlencode(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    session.post('https://www.funda.nl/mijn/login/', data=raw, cookies=sessionCookies, headers=headers)

    links = list()
    resp = session.get(BEWRD_URL + 'p1')
    soup = BeautifulSoup(resp.text, "html5lib")

    pagelinks = soup.find_all("a", attrs={"data-pagination-page":True})
    pages = []
    for page in pagelinks:
        pages.append(int(page["data-pagination-page"]))
    einde = max(pages) + 1

    for i in range(1, einde):
        links.append(BEWRD_URL + 'p' + str(i))

    for page in links:
        html = session.get(page)
        soup = BeautifulSoup(html.text, "html5lib")
        houses = soup.find('ul', class_='search-results').find_all('li', class_="search-result ")
        for house in houses:
            raw_address = house.find('h3', class_='search-result-title').text

            raw_address_list = [s.strip() for s in raw_address.splitlines()]
            street_nr = raw_address_list[1]
            postalcode_city = raw_address_list[3]
            postcode = postalcode_city[:7]
            city = postalcode_city[8: ]
            lnk = "http://www.funda.nl" + house.find('a', href=True)['href']
            object_handle = house.find('a', class_='remove-object-handle')['href']
            funda_id = int(object_handle.split('tinyId=')[1])
            image_src = house.find('img')['src']

            try:
                price = int(unidecode.unidecode(house.find('span', class_='search-result-price').text).replace("EUR ", "").replace(".", "").replace("kk",""))
            except ValueError:
                price = 0
            try:
                woonopp = int(house.find('span', title="Woonoppervlakte").text.split(' ')[0])
            except ValueError:
                woonopp = 0
            try:
                percopp = int(house.find('span', title="Perceeloppervlakte").text.split(' ')[0].replace(".", ""))
            except ValueError:
                percopp = 0
            if woonopp == 0:
                sqprice = 0
            else:
                sqprice = price / woonopp

            #pcode = street_nr + " " + postalcode_city
            pcode = street_nr + " " + postcode
            url = GEOCODE_URL + pcode
            response = requests.get(url)
            try:
                # see http://gis.stackexchange.com/questions/58271/using-python-to-parse-an-xml-containing-gml-tags
                root = ET.fromstring(response.content)
                for point in root.findall('.//{http://www.opengis.net/gml}Point'):
                    rdxy = point.findtext("{http://www.opengis.net/gml}pos").split()
                pnt = GEOSGeometry('POINT({0} {1})'.format(rdxy[0], rdxy[1]), srid=28992)
                # see http://gis.stackexchange.com/questions/94640/geodjango-transform-not-working
                pnt.transform(4326)
            except:
                rdxy = [0, 0]
                pnt = GEOSGeometry('POINT({0} {1})'.format(0, 0), srid=4326)

            cm = House.objects.create(
                fuid=funda_id,
                image=image_src,
                address=street_nr + ' ' + postalcode_city,
                strnumr=street_nr,
                postcod=postcode,
                plaprov=city,
                woonopp=woonopp,
                percopp=percopp,
                vrprijs=price,
                sqprijs=sqprice,
                link=lnk,
                dellink='http://www.funda.nl' + object_handle,
                rdx=rdxy[0],
                rdy=rdxy[1],
                lat=pnt.y,
                lon=pnt.x,
                sender='backend',
                channel='homepage',
                content='yo',
                geom=pnt
            )

            #t = loader.get_template('message.html')
            hxdispatcher.send(cm.channel, {
                #'html': t.render(Context({'message': cm})),
                'fuid': funda_id,
                'image': image_src,
                'address': street_nr + ' ' + postalcode_city,
                'strnumr': street_nr,
                'postcod': postcode,
                'plaprov': city,
                'woonopp': woonopp,
                'percopp': percopp,
                'vrprijs': price,
                'sqprijs': sqprice,
                'link': lnk,
                'dellink': 'http://www.funda.nl' + object_handle,
                'lat': pnt.y,
                'lon': pnt.x
            })

