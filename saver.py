import os
import requests
import time
from bs4 import BeautifulSoup
import re

# create folder for pages (if not exists)
if not os.path.exists('pages'):
    os.mkdir('pages')

# base URL
base_url = 'https://auto.drom.ru/bmw/x1/'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

# get response from base URS
response = requests.get(base_url, headers=headers)
# change encoding
site_encoding = 'cp1251'
response.encoding = site_encoding
print(f'response status code: {response.status_code}')

# check response from base URL is 200
if response.status_code != 200:
    exit('Error: bad response')

# get number of pages for scraping
soup = BeautifulSoup(response.content, 'html.parser')
# get data from search table
buttons = soup.find_all('button', {'data-ftid' : 'component_select_button'})
# get number of cars from second input field button
cars_number = buttons[1].get_text()
# clean number and divide by 20 cars per page
pages_number = int(int(re.search(r'\((\d*)\)', cars_number).group(1)) / 20 + 1)
print(f'number of pages for scaping: {pages_number}')

# start saving pages
for page in range(1, pages_number + 1):
    
    # URL page
    url = base_url + 'page' + str(page)
    
    # scrape page and change encoding
    time.sleep(2)
    print(url, end='')
    response = requests.get(url, headers=headers)
    response.encoding = site_encoding
    print(f': {response.status_code} ...', end=' ')
    
    filename = 'pages/page' + str(page) + '.html'
    with open(filename, 'wb') as file:
        file.write(response.content)
        print('saved!')