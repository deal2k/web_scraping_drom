from bs4 import BeautifulSoup
from itertools import zip_longest
import pandas as pd
import csv
import re

site_encoding = 'cp1251'
pages_number = 23

# prepare list to store results
cars = []

# start scraping pages
for page in range(1, pages_number + 1):
    
    # selecting HTML file for scraping
    filename = 'pages/page' + str(page) + '.html'
    print(f'scraping {filename}')
    
    # open html page
    with open(filename, encoding=site_encoding) as file:
        html = file.read()
    
    soup = BeautifulSoup(html, 'html.parser')  
    
    # collect repeated cards of cars
    cards = soup.find_all('a', {'data-ftid' : 'bulls-list_bull'})
    for card in cards:
        # prepare "car" dictionary to store values
        car = {}
        
        # get car name in format "BMW X1, 2009"
        car_name = card.find('span', {'data-ftid' : 'bull_title'}).string
        # keep only year for dataset
        car['year'] = int(car_name[-4:])
        
        # car price data contained comment "<!-- -->" inside
        # remove comment from tag
        price0 = card.find('span', {'data-ftid' : 'bull_price'}).prettify().split('<!-- -->')
        # remove new line "\n" characters
        price1 = [block.split('\n') for block in price0]
        # select only price form 2d list, remove spaces and save to dict
        car['price'] = int(price1[0][1].replace(' ', ''))
        
        # location of the car
        location = card.find('span', {'data-ftid' : 'bull_location'}).string
        # remove ", " characters from end of string and save to dict
        car['location'] = location
        
        # description of the car
        # define description columns
        desc_col = ['motor', 'fuel', 'transmission', 'drive', 'mileage']
        # collect in list all description items
        desc_items = [card.get_text() for card in card.find_all('span', {'data-ftid' : 'bull_description-item'})]
        
        # sometimes description item 6 (color) added
        if len(desc_items) > 5:
            desc_items = desc_items[:-1]
        
        # make iterable zip object and save cleaned values to table
        for col, desc in zip_longest(desc_col, desc_items, fillvalue=None):
            # remove "," from end of string
            if desc != None:
                desc = desc.strip(',')
            car[col] = desc
        
        # get engine volume
        volume = car['motor'][:3]
        #volume = re.search(r'(\d.\d)\wл', car['motor']).group(1)
        try:
            car['volume'] = float(volume)
        except ValueError:
            pass
        
        # get engine power
        if re.search(r'(\d\d\d)', car['motor']) != None:
            car['power'] = re.search(r'(\d\d\d)', car['motor']).group(1)
        
        # keep only values of km from string "XXX thousend km"
        if car['mileage'] != None:
            car['mileage'] = re.search(r'(\d*)', car['mileage']).group(1)
        elif car['year'] >= 2020:
            car['mileage'] = 0
            if car['year'] == 2021:
                car['year'] = 2020
        else:
            car['mileage'] = None
        
        # add car to cars list
        cars.append(car)

with open('cars.csv', 'w') as file:
    writer = csv.DictWriter(file, cars[0].keys())
    writer.writeheader()
    writer.writerows(cars)

#df = pd.DataFrame(cars)
#df.to_csv('cars.csv')