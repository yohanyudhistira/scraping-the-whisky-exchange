import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.thewhiskyexchange.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

product_links = []

for x in range(1, 6):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}&psize=24&sort=pasc')
    soup = BeautifulSoup(r.content, 'lxml')

    products_list = soup.find_all('li', class_='product-grid__item')

    for item in products_list:
        for link in item.find_all('a', href=True):
            product_links.append(base_url + link['href'])

whisky_list = []
for link in product_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='product-main__name').text.strip()
    price = soup.find('p', class_='product-action__price').text.strip()
    try:
        rating = soup.find('div', class_='review-overview').text.strip().replace('\n', '')
    except:
        rating = 'no rating'
    whisky = {
        'name': name,
        'rating': rating,
        'price': price,
    }
    whisky_list.append(whisky)
    print('Scraping:', whisky['name'])

df = pd.DataFrame(whisky_list)
print(df.head())
df.to_csv('whisky.csv', index=False)
