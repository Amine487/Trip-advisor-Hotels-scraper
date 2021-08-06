import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import requests

records = []
hrefs = []

for n in range(2, 10, 2):    
    url = 'https://www.tripadvisor.com/Hotels-g{0}-Hotels.html'.format(n)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for n in range(20):    
        geo_id_0 = soup.find('div', {'class': 'leaf_geo_list_wrapper entry_point_update'}).findAll('a')[n]['href']
        hrefs.append(geo_id_0)

    LP = soup.find('a', attrs={'class': 'pageNum last'}).text
    for i in range(20, int(LP), 20):
        url2 = url[:38] + 'oa{0}'.format(i) + '-Hotels.html'
        r2 = requests.get(url2)
        soup2 = BeautifulSoup(r2.text, 'html.parser')

        for x in range(20):
            geo_id_1 = soup2.find('ul', {'class': 'geoList ui_columns is-multiline'}).findAll('a')[x]['href']
            hrefs.append(geo_id_1)
            
for b in range(len(hrefs)):
    url3 = 'https://www.tripadvisor.com/' + hrefs[b]
    r3 = requests.get(url3)
    soup3 = BeautifulSoup(r3.text, 'html.parser')
    container = soup3.find_all('div', attrs={'class', 'ui_column is-8 main_col allowEllipsis'})

    city_name = soup3.find('h1', {'class': 'page_h1_line1'}).text

    for i in container:
        hotel_name = i.find('div', 'listing-title').text.strip()

        hotel_price = i.findAll('div', attrs={'class': 'price autoResize'})
        li = []
        for m in hotel_price:
            if len(m.text) > 0:
                x = m.text.replace('$', '').replace(',', '').strip()
                li.append(int(x))
                hotel_price = np.mean(li)
            else:
                hotel_price = []

        hotel_reviews_count = i.find('a', 'review_count').text
        try:
            hotel_reviews = i.find('div', {"class": "prw_rup prw_common_rating_and_review_count_with_popup linespace is-shown-at-mobile"}).findAll('a')[0]['alt'][:4].strip()
        except:
            hotel_reviews = []

        hotel_info = i.find('div', {'class': 'info-col'}).findAll('span', {'class', 'text'})
        info = []
        x = 0
        for y in hotel_info:
            info.append(hotel_info[x].text)
            x += 1

        try:
            hotel_offers = i.find('div', {'class': 'prw_rup prw_hotels_merchandise_messages'}).findAll('span')
        except:
            hotel_offers = []

        info2 = []
        x = 0

        for n in hotel_offers:
            try:
                if len(hotel_offers[x].text) > 0:
                    info2.append(hotel_offers[x].text)
                x +=1
            except:
                hotel_offers[x] = []
                
        x = int(len(soup3.find('div', attrs={'id': 'taplc_trip_planner_breadcrumbs_0'}).findAll('li'))) - 2
        continent_name = soup3.find('div', attrs={'id': 'taplc_trip_planner_breadcrumbs_0'}).findAll('li')[0].text
        country_name = soup3.find('div', attrs={'id': 'taplc_trip_planner_breadcrumbs_0'}).findAll('li')[1].text
        city_name = soup3.find('div', attrs={'id': 'taplc_trip_planner_breadcrumbs_0'}).findAll('li')[x].text

        records.append((hotel_name, continent_name, city_name, country_name, hotel_price, hotel_reviews, hotel_reviews_count, info, info2))
        
df_TA = pd.DataFrame(records, columns=['Hotel name', 'continent_name', 'country_name', 'city_name', 'Price', 'Rating', 'reviews count', 'info', 'info2'])

df_TA.to_csv('TA hotels.csv')